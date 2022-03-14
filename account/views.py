from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework_jwt.settings import api_settings
from service.utils.country_code import CountryCode
from service.utils.mobile_number import prefix_country_code
from account.choice import EXCLUDE_GROUP
from account.hmac import EmailConfirmationHMAC
from account.models import Address, User, UserEmail, UserMobileNumber, UserPhotos
from account.permission import (
    AddressPermission,
    AuthenticationPermission,
    ProfilePermission,
    ProfilePhotoPermission,
)
from account.serializers import (
    AddressCRUDSerializer,
    AddressReadOnlyGeoLocationSerializer,
    GroupCRUDSerializer,
    JWTSerializer,
    LoginSerializer,
    MobileSerializer,
    MutationProfileSerializer,
    OTPValidationSerializer,
    PasswordChangeSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
    PermissionCRUDSerializer,
    PhotosCRUDSerializer,
    ProfileSerializer,
    RegisterSerializer,
    ReSendSerializer,
    SendSerializer,
    UserSerializer,
    VerifyEmailSerializer,
)
from account.tasks import resend_otp, send_otp, verify_otp
from base.permission import AdminPermission, IsAuthenticatePermission
from base.response import Response
from base.validators import validate_international_phonenumber


class AuthenticationViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, AuthenticationPermission]

    def get_email(self, email):
        try:
            return UserEmail.objects.get(email=email)
        except UserEmail.DoesNotExist:
            raise ValidationError(
                detail={"username": "Email address are not found!"},
                code=status.HTTP_404_NOT_FOUND,
            )

    def get_group(self, type):
        try:
            return Group.objects.get(name=type)
        except Group.DoesNotExist:
            raise ValidationError(
                detail={"message": "Permission group are not found!"},
                code=status.HTTP_404_NOT_FOUND,
            )

    @action(
        detail=False,
        methods=["POST"],
        url_path="otp/send",
    )
    def otp_send(self, request, *args, **kwargs):
        serializer = SendSerializer(data=request.data)
        instance = None
        if serializer.is_valid(raise_exception=True):
            validate_international_phonenumber(request.data.get("mobile_number"))
            mobile_number = prefix_country_code(
                CountryCode.INDIA, str(request.data.get("mobile_number"))
            )
            try:
                instance = UserMobileNumber.objects.get(mobile_number=mobile_number)
                serializer = SendSerializer(instance=instance, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.update(instance, serializer.validated_data)
            except UserMobileNumber.DoesNotExist:
                with transaction.atomic():
                    instance = serializer.save()

            if instance:
                send_otp.delay(instance.mobile_number)
                serializer = MobileSerializer(instance=instance)
                return Response(
                    serializer.data,
                    message="Message are sent.",
                    status=status.HTTP_200_OK,
                )
        return Response(message="Message not sent.", status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["POST"],
        url_path="otp/verify",
    )
    def otp_verify(self, request, *args, **kwargs):
        serializer = OTPValidationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            try:
                instance = UserMobileNumber.objects.get(
                    mobile_number=data.get("mobile_number")
                )
            except Exception:
                raise ValidationError(
                    detail={"mobile_number": "User not found!"},
                    code=status.HTTP_404_NOT_FOUND,
                )

            response = verify_otp(
                instance.mobile_number, otp_value=data.get("otp", 0000)
            )
            if (
                response.get("success", False)
                or response.get("error") == "Mobile no. already verified"
            ):
                # if user has not active set as active
                if not instance.user.is_active:
                    User.objects.filter(pk=instance.user.pk).update(is_active=True)

                instance.verify = True
                instance.save()

                # JWT token process
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(instance.user)
                payload["user_id"] = str(payload["user_id"])
                token = jwt_encode_handler(payload)
                # JWT token process

                # Django login
                django_login(self.request, instance.user)
                # Django login

                data = {"user": instance.user, "token": token}
                serializer = JWTSerializer(
                    instance=data, context={"request": self.request}
                )
                expiration = timezone.now() + api_settings.JWT_EXPIRATION_DELTA
                response = Response(
                    serializer.data,
                    message="OTP has successfully valid!.",
                    status=status.HTTP_200_OK,
                )
                response.set_cookie(
                    api_settings.JWT_AUTH_COOKIE,
                    token,
                    expires=expiration,
                    httponly=True,
                )
                return response
            else:
                message = response.get("error", "OTP has not valid or expired!.")
                raise ValidationError({"otp": message})

        return Response(
            message="OTP has not valid or expired!.",
            status=status.HTTP_401_UNAUTHORIZED,
        )

    @action(
        detail=False,
        methods=["POST"],
        url_path="otp/resend",
    )
    def otp_resend(self, request, *args, **kwargs):
        serializer = ReSendSerializer(data=request.data)
        instance = None
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            try:
                instance = UserMobileNumber.objects.get(
                    mobile_number=data.get("mobile_number")
                )
            except UserMobileNumber.DoesNotExist:
                pass

            if instance:
                message = "Successfully resend OTP."
                response = resend_otp(
                    instance.mobile_number, retry_type=data.get("retry_type", "text")
                )
                return_message = (
                    response.get("error")
                    if response.get("error", "")
                    else response.get("success", "")
                )
                final_message = return_message or message
                return Response(
                    message=final_message,
                    status=status.HTTP_200_OK,
                )
        return Response(message="Mobile not found!.", status=status.HTTP_404_NOT_FOUND)

    @action(
        detail=False,
        methods=["POST"],
    )
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get("user")

            # JWT token process
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            payload["user_id"] = str(payload["user_id"])
            token = jwt_encode_handler(payload)
            # JWT token process

            data = {"user": user, "token": token}
            serializer = JWTSerializer(instance=data, context={"request": self.request})
            expiration = timezone.now() + api_settings.JWT_EXPIRATION_DELTA

            # Django login
            django_login(self.request, user)
            # Django login

            response = Response(
                serializer.data,
                message="Login successfully!",
                status=status.HTTP_200_OK,
            )
            response.set_cookie(
                api_settings.JWT_AUTH_COOKIE,
                token,
                expires=expiration,
                httponly=True,
            )
            return response
        return Response(
            message="Unauthorized user.",
            status=status.HTTP_401_UNAUTHORIZED,
        )

    @action(
        detail=False,
        methods=["POST"],
    )
    def logout(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        # Django logout
        django_logout(request)
        # Django logout

        response = Response(
            message="Successfully logged out!.", status=status.HTTP_200_OK
        )

        # DELETE jwt auth cookie if exist
        response.delete_cookie(
            api_settings.JWT_AUTH_COOKIE
        ) if api_settings.JWT_AUTH_COOKIE else None

        return response

    @action(
        detail=False,
        methods=["POST"],
        url_path="password/reset",
    )
    def password_reset(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get("email")
            email_object = self.get_email(email=email)
            email_confirmation_hmac = EmailConfirmationHMAC(email_object)
            email_confirmation_hmac.reset_password(request=request)
            return Response(
                message="Password reset e-mail has been sent.",
                status=status.HTTP_200_OK,
            )
        # Return the success message with OK HTTP status
        return Response(
            message="Password rest e-mail has not been sent.",
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=False,
        methods=["POST"],
        url_path="password/change",
    )
    def password_change(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                email_object = UserEmail.objects.get(user=request.user, primary=True)
            except UserEmail.DoesNotExist:
                raise ValidationError(
                    detail={"email": "Current, email are not found."},
                    code=status.HTTP_404_NOT_FOUND,
                )
            email_confirmation = EmailConfirmationHMAC(email_object=email_object)
            email_confirmation.change_password(request=request)
            serializer.save()
            return Response(
                message="New password has been saved.", status=status.HTTP_200_OK
            )
        return Response(
            message="Password not saved.", status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        methods=["POST"],
        url_path="password/reset/confirm",
    )
    def password_reset_confirm(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                message="Password has been reset with the new password.",
                status=status.HTTP_200_OK,
            )
        return Response(
            message="Password has been not reset with the new password.",
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=False,
        methods=["POST"],
    )
    def signup(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_email = None
            data = serializer.validated_data
            username = data.get("username")
            password = data.get("password")

            if username:
                user_email = UserEmail.objects.filter(
                    email=username, primary=True
                ).first()
                if user_email:
                    username = user_email.email

            if User.objects.filter(username=username).exists():
                raise ValidationError({"username": "This username is already exists."})

            user_instance = User.objects.create_user(
                username=username, password=password
            )

            if data.get("group_ids", []):
                for group in data.get("group_ids"):
                    user_instance.groups.add(group)

            if username:
                UserEmail.objects.add_email(
                    request, user_instance, username, confirm=True, signup=True
                )
        return Response(
            message="Signup confirmation e-mail has been sent.",
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=False,
        methods=["POST"],
        url_path="email/verify",
    )
    def email_verify(self, request, *args, **kwargs):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            key = serializer.validated_data.get("key")
            email_confirmation = EmailConfirmationHMAC()
            email_confirmation_object = email_confirmation.from_key(key)
            if email_confirmation_object:
                email_confirmation_object.set_verify()
                return Response(
                    message="Email has successfully verified",
                    status=status.HTTP_200_OK,
                )
        return Response(
            message="This email is can't verify", status=status.HTTP_400_BAD_REQUEST
        )


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.exclude(is_deleted=True)
    serializer_class = ProfileSerializer
    http_method_names = [
        "get",
        "head",
        "patch",
    ]
    permission_classes = [IsAuthenticatePermission, ProfilePermission]

    def get_serializer_class(self):
        if self.action in ["patch", "update", "partial_update"]:
            return MutationProfileSerializer
        else:
            return ProfileSerializer


class UserPhotosViewSet(viewsets.ModelViewSet):
    queryset = UserPhotos.objects.exclude(is_deleted=True)
    serializer_class = PhotosCRUDSerializer
    http_method_names = [
        "get",
        "head",
        "post",
        "patch",
        "delete",
    ]
    permission_classes = [IsAuthenticatePermission, ProfilePhotoPermission]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return UserPhotos.objects.none()

        queryset = self.queryset

        if self.request.user:
            if self.request.user.is_superuser:
                return queryset
            return queryset.filter(user=self.request.user)
        return queryset.none()


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.exclude(is_deleted=True)
    serializer_class = AddressCRUDSerializer
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [IsAuthenticatePermission, AddressPermission]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Address.objects.none()

        queryset = self.queryset
        if self.request.user:
            if self.request.user.is_superuser:
                return queryset
            return queryset.filter(user=self.request.user)
        return queryset.none()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return AddressReadOnlyGeoLocationSerializer
        return self.serializer_class


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupCRUDSerializer
    http_method_names = ["get", "post", "head", "patch", "delete"]
    permission_classes = [AdminPermission]


class GroupReadOnlyViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.exclude(name__in=EXCLUDE_GROUP)
    http_method_names = [
        "get",
        "head",
    ]
    serializer_class = GroupCRUDSerializer
    permission_classes = [AllowAny]


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    http_method_names = ["get", "post", "head", "patch", "delete"]
    serializer_class = PermissionCRUDSerializer
    permission_classes = [AdminPermission]

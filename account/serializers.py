from base.serializers import BaseSerializer
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _
from drf_extra_fields.fields import Base64ImageField
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from service.utils.country_code import CountryCode
from service.utils.mobile_number import prefix_country_code
from v1.membership.calculation import customer_has_exist_membership
from v1.package.models import PackageBoy

from account.authentication_backend import custom_authenticate
from account.choice import EXCLUDE_GROUP, RetryType, SystemDefaultGroup
from account.hmac import EmailConfirmationHMAC
from account.utils import email_is_valid, get_projects_apps_models

from .models import Address, User, UserEmail, UserMobileNumber, UserPhotos


def mobile_number_validate(attrs):
    if attrs.get("mobile_number"):
        attrs["mobile_number"] = prefix_country_code(
            CountryCode.INDIA, str(attrs.get("mobile_number"))
        )
    return attrs


class PermissionCRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            "id",
            "name",
            "codename",
        )


class GroupCRUDSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Group
        fields = "__all__"

    def get_permissions(self, obj):
        if not obj.permissions:
            return []
        return PermissionCRUDSerializer(obj.permissions, many=True).data


class PhotosCRUDSerializer(BaseSerializer):
    photo = Base64ImageField(required=False)
    user_id = serializers.SlugRelatedField(
        slug_field="id",
        queryset=User.objects.exclude(is_deleted=True),
        required=True,
        source="user",
        write_only=True,
    )

    class Meta:
        model = UserPhotos
        fields = "__all__"
        read_only_fields = ("user",)


class EmailSerializer(BaseSerializer):
    class Meta:
        model = UserEmail
        fields = "__all__"
        read_only_fields = ("user",)

    def validate(self, attrs):
        if self.context.get("user"):
            attrs["user"] = self.context.get("user")
        return attrs


class EmailGettingTimeSerializer(BaseSerializer):
    id = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=UserEmail.objects.exclude(is_deleted=True),
    )

    class Meta:
        model = UserEmail
        fields = "__all__"


class MobileSerializer(BaseSerializer):
    class Meta:
        model = UserMobileNumber
        fields = "__all__"
        read_only_fields = ("user",)

    def validate(self, attrs):
        if self.context.get("user"):
            attrs["user"] = self.context.get("user")
        return attrs


class MobileGettingSerializer(BaseSerializer):
    id = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=UserMobileNumber.objects.exclude(is_deleted=True),
    )

    class Meta:
        model = UserMobileNumber
        fields = "__all__"


class UserSerializer(BaseSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "groups",
            "user_permissions",
        )


class AddressCRUDSerializer(BaseSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.SlugRelatedField(
        slug_field="id",
        queryset=User.objects.exclude(is_deleted=True),
        required=False,
        source="user",
        write_only=True,
    )

    class Meta:
        model = Address
        fields = "__all__"

    def validate(self, attrs):
        if attrs.get("is_set_manually", False) == False and not attrs.get(
            "geo_location", None
        ):
            raise ValidationError(
                {
                    "geo_location": "While geo location are empty then set `is_set_manually:true` rather then, please adding geo location."
                }
            )
        return attrs

    def to_representation(self, instance):
        instance = super(AddressCRUDSerializer, self).to_representation(instance)
        return instance


class AddressReadOnlyGeoLocationSerializer(BaseSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = (
            "user",
            "geo_location",
        )


class ProfileSerializer(BaseSerializer):
    mobile_number = serializers.SerializerMethodField(read_only=True)
    emails = serializers.SerializerMethodField(read_only=True)
    address = serializers.SerializerMethodField(read_only=True)
    photos = serializers.SerializerMethodField(read_only=True)
    groups = GroupCRUDSerializer(many=True, read_only=True)
    customer_has_exist_membership = serializers.SerializerMethodField(read_only=True)
    delivery_boy_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "is_superuser",
            "first_name",
            "last_name",
            "father_name",
            "emails",
            "mobile_number",
            "address",
            "photos",
            "groups",
            "date_of_birth",
            "is_profile_completely_filled",
            "customer_has_exist_membership",
            "delivery_boy_id",
            "referral_code",
            "is_online",
        )
        read_only_fields = (
            "id",
            "is_active",
            "is_staff",
            "last_login",
            "is_superuser",
            "delivery_boy_id",
            "referral_code",
        )

    def get_delivery_boy_id(self, obj):
        if hasattr(obj, "delivery_boy_user") and obj.delivery_boy_user.first():
            return obj.delivery_boy_user.first().pk
        return None

    def get_customer_has_exist_membership(self, obj):
        return customer_has_exist_membership(customer=obj)

    def get_mobile_number(self, obj):
        items = UserMobileNumber.objects.filter(user=obj).exclude(is_deleted=True)
        if items:
            return MobileSerializer(items, many=True).data
        return []

    def get_emails(self, obj):
        items = UserEmail.objects.filter(user=obj).exclude(is_deleted=True)
        if items:
            return EmailSerializer(items, many=True).data
        return []

    def get_address(self, obj):
        items = Address.objects.filter(user=obj).exclude(is_deleted=True)
        if items:
            return AddressReadOnlyGeoLocationSerializer(items, many=True).data
        return []

    def get_photos(self, obj):
        items = UserPhotos.objects.filter(user=obj).exclude(is_deleted=True)
        if items:
            return PhotosCRUDSerializer(
                items, many=True, context={"request": self.context.get("request")}
            ).data
        return []


class MutationProfileSerializer(BaseSerializer):
    user_mobile_number = MobileGettingSerializer(many=True, required=False)
    user_email = EmailGettingTimeSerializer(many=True, required=False)
    groups = GroupCRUDSerializer(many=True, read_only=True)
    group_ids = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Group.objects.all(),
        source="groups",
        many=True,
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "father_name",
            "date_of_birth",
            "is_profile_completely_filled",
            "user_email",
            "user_mobile_number",
            "groups",
            "group_ids",
            "is_online",
        )
        read_only_fields = (
            "username",
            "referral_code",
        )

    def create(self, validated_data):
        user_mobile_number = validated_data.pop("user_mobile_number", None)
        user_email = validated_data.pop("user_email", None)

        user = super(MutationProfileSerializer, self).create(validated_data)
        if user_mobile_number:
            for mobile_number in user_mobile_number:
                mobile_number_serializer = MobileSerializer(
                    data=mobile_number, context={"user": user}
                )
                if mobile_number_serializer.is_valid(raise_exception=True):
                    mobile_number_serializer.save()
        if user_email:
            for email in user_email:
                emails_serializer = EmailSerializer(data=email, context={"user": user})
                if emails_serializer.is_valid(raise_exception=True):
                    emails_serializer.save()

        return user

    def update(self, instance, validated_data):
        user_mobile_number = validated_data.pop("user_mobile_number", None)
        user_email = validated_data.pop("user_email", None)
        user = super(MutationProfileSerializer, self).update(instance, validated_data)
        if user_mobile_number:
            for mobile_number in user_mobile_number:
                mobile_number_instance = None

                if mobile_number.get("id"):
                    mobile_number_instance = mobile_number.pop("id")

                if mobile_number_instance:
                    mobile_number_serializer = MobileSerializer(
                        instance=mobile_number_instance,
                        data=mobile_number,
                        context={"user": user},
                    )
                    if mobile_number_serializer.is_valid(raise_exception=True):
                        mobile_number_serializer.update(
                            instance=mobile_number_instance,
                            validated_data=mobile_number,
                        )
                else:
                    mobile_number_serializer = MobileSerializer(
                        data=mobile_number, context={"user": user}
                    )
                    if mobile_number_serializer.is_valid(raise_exception=True):
                        mobile_number_serializer.save()

        if user_email:
            for email in user_email:
                email_instance = None

                if email.get("id"):
                    email_instance = email.pop("id")

                if email_instance:
                    email_serializer = EmailSerializer(
                        instance=email_instance,
                        data=email,
                        context={"user": user},
                    )
                    if email_serializer.is_valid(raise_exception=True):
                        email_serializer.update(
                            instance=email_instance,
                            validated_data=email,
                        )
                else:
                    emails_serializer = EmailSerializer(
                        data=email, context={"user": user}
                    )
                    if emails_serializer.is_valid(raise_exception=True):
                        emails_serializer.save()

        return user


class SendSerializer(BaseSerializer):
    mobile_number = serializers.CharField(required=True)
    group_ids = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Group.objects.all(),
        many=True,
        write_only=True,
    )

    class Meta:
        model = UserMobileNumber
        fields = (
            "mobile_number",
            "group_ids",
        )

    def validate(self, attrs):
        attrs = mobile_number_validate(attrs)
        group_ids = attrs.get("group_ids", [])
        if group_ids:
            allowed_group = Group.objects.exclude(name__in=EXCLUDE_GROUP)
            for group in group_ids:
                if group.name == SystemDefaultGroup.PACKAGING_STAFF:
                    try:
                        PackageBoy.objects.get(mobile_number=attrs["mobile_number"])
                    except Exception:
                        raise ValidationError(
                            {
                                "mobile_number": "You are not allowed for login in package application!."
                            }
                        )

                if not group in allowed_group:
                    raise ValidationError({"group_ids": "Not allowed this group!."})
        else:
            raise ValidationError({"group_ids": "Group ids are not found!."})
        return attrs

    def create(self, validated_data):
        group_ids = validated_data.pop("group_ids", [])
        instance = super(SendSerializer, self).create(validated_data)
        user_name_serializer = UserSerializer(
            data={"username": str(instance.mobile_number)}
        )
        if user_name_serializer.is_valid(raise_exception=True):
            user_instance = user_name_serializer.save()
            if group_ids:
                for group in group_ids:
                    user_instance.groups.add(group)
            instance.user = user_instance
            instance.save()
        return instance

    def update(self, instance, validated_data):
        group_ids = validated_data.pop("group_ids", [])
        instance = super(SendSerializer, self).update(instance, validated_data)
        if group_ids:
            for group in group_ids:
                instance.user.groups.add(group)
        return instance


class ReSendSerializer(BaseSerializer):
    retry_type = serializers.ChoiceField(
        choices=RetryType.choices, default=RetryType.TEXT
    )
    mobile_number = serializers.CharField(required=True)

    class Meta:
        model = UserMobileNumber
        fields = (
            "mobile_number",
            "retry_type",
        )

    def validate(self, attrs):
        attrs = mobile_number_validate(attrs)
        return super().validate(attrs)


class OTPValidationSerializer(BaseSerializer):
    otp = serializers.CharField(required=True)
    mobile_number = serializers.CharField(required=True)

    class Meta:
        model = UserMobileNumber
        fields = (
            "otp",
            "mobile_number",
        )

    def validate(self, attrs):
        attrs = mobile_number_validate(attrs)
        return super().validate(attrs)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(style={"input_type": "password"})

    def verify_mobile_number(self, user, mobile_number):
        mobile_number = user.user_mobile_number.filter(
            mobile_number=mobile_number, is_deleted=False
        ).first()
        if mobile_number and not mobile_number.verify:
            raise serializers.ValidationError(
                {"username": _("Mobile number is not verified.")}
            )

    def verify_email(self, user, email):
        email_address = user.user_email.filter(email=email, is_deleted=False).first()
        if email_address and not email_address.verify:
            raise serializers.ValidationError(
                {"username": _("E-mail is not verified.")}
            )

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        user = custom_authenticate(username=username)

        # Did we get back an active user?
        if user:
            if not user.check_password(password):
                msg = _("Invalid password.")
                raise exceptions.ValidationError({"password": msg})

            if not user.is_active:
                msg = _("User account is disabled.")
                raise exceptions.ValidationError({"user": msg})
        else:
            msg = _("Unable to log in with provided credentials.")
            raise exceptions.ValidationError({"user": msg})

        if str(username).isnumeric():
            mobile_number_username = prefix_country_code(
                CountryCode.INDIA, str(username)
            )
            self.verify_mobile_number(user, mobile_number_username)

        elif "@" in str(username):
            if not email_is_valid(username):
                raise serializers.ValidationError(
                    {"email": _("E-mail is not valid format.")}
                )
            self.verify_email(user, username)

        attrs["user"] = user
        return attrs


class JWTSerializer(serializers.Serializer):
    """
    Serializer for JWT authentication.
    """

    token = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        """
        Required to allow using custom USER_DETAILS_SERIALIZER in
        JWTSerializer. Defining it here to avoid circular imports
        """
        user_data = ProfileSerializer(obj["user"], context=self.context).data
        return user_data


class PasswordResetSerializer(BaseSerializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    email = serializers.EmailField(required=True)

    class Meta:
        model = UserEmail
        fields = "__all__"


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    def validate(self, attrs):
        self._errors = {}
        email_object = EmailConfirmationHMAC().from_key(key=attrs.get("token"))

        try:
            self.user = User._default_manager.get(pk=email_object.user.pk)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError(
                {"token": "User are not found for this token or expired."}
            )

        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        return self.set_password_form.save()


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.logout_on_password_change = True
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

        self.fields.pop("old_password")

        self.request = self.context.get("request")
        self.user = getattr(self.request, "user", None)

    def validate_old_password(self, value):
        if self.user and not self.user.check_password(value):
            raise serializers.ValidationError({"password": "Invalid password"})
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash

            update_session_auth_hash(self.request, self.user)


class RegisterSerializer(BaseSerializer):
    username = serializers.CharField(max_length=50, min_length=8, required=True)
    password1 = serializers.CharField(max_length=128, min_length=8)
    password2 = serializers.CharField(max_length=128, min_length=8)
    group_ids = serializers.SlugRelatedField(
        required=False,
        slug_field="id",
        queryset=Group.objects.filter(
            permissions__content_type__app_label__in=get_projects_apps_models()
        ),
        many=True,
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
            "group_ids",
        )

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password2": _("The two password fields didn't match.")}
            )
        else:
            attrs["password"] = attrs["password1"]
        return attrs


class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField()

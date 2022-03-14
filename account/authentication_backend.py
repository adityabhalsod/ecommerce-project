from threading import local

from django.contrib.auth.backends import ModelBackend

from service.utils.country_code import CountryCode
from service.utils.mobile_number import prefix_country_code
from account.models import User, UserEmail, UserMobileNumber

_stash = local()


def custom_authenticate(request=None, username=None, password=None, **kwargs):
    mobile_number = None
    email_address = None
    user = None

    try:
        email_address = UserEmail.objects.get(email=username)
    except UserEmail.DoesNotExist:
        email_address = None

    try:
        mobile_number = prefix_country_code(CountryCode.INDIA, str(user))
        mobile_number = UserMobileNumber.objects.get(mobile_number=username)
    except UserMobileNumber.DoesNotExist:
        mobile_number = None

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None

    if email_address:
        return email_address.user
    elif mobile_number:
        return mobile_number.user
    elif user:
        return user

    return None


class AuthBackend(ModelBackend):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = custom_authenticate(request, username, password, **kwargs)
        ret = self.user_can_authenticate(user)
        if not ret:
            self._stash_user(user)
        return user

    @classmethod
    def _stash_user(cls, user):
        """Now, be aware, the following is quite ugly, let me explain:

        Even if the user credentials match, the authentication can fail because
        Django's default ModelBackend calls user_can_authenticate(), which
        checks `is_active`. Now, earlier versions of allauth did not do this
        and simply returned the user as authenticated, even in case of
        `is_active=False`. For allauth scope, this does not pose a problem, as
        these users are properly redirected to an account inactive page.

        This does pose a problem when the allauth backend is used in a
        different context where allauth is not responsible for the login. Then,
        by not checking on `user_can_authenticate()` users will allow to become
        authenticated whereas according to Django logic this should not be
        allowed.

        In order to preserve the allauth behavior while respecting Django's
        logic, we stash a user for which the password check succeeded but
        `user_can_authenticate()` failed. In the allauth authentication logic,
        we can then unstash this user and proceed pointing the user to the
        account inactive page.
        """
        global _stash
        ret = getattr(_stash, "user", None)
        _stash.user = user
        return ret

    @classmethod
    def unstash_authenticated_user(cls):
        return cls._stash_user(None)

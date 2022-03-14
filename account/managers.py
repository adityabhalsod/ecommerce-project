from datetime import timedelta

from constance import config
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.gis.db import models
from django.utils import timezone

from account import utils


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError("The given username must be set")

        user = self.model(username=username, **extra_fields)
        if password:
            # if password is exist then set password other wise skip save password
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)


class EmailAddressManager(models.Manager):
    def can_add_email(self, user):
        ret = True
        if config.MAX_EMAIL_ADDRESSES:
            count = self.filter(user=user).count()
            ret = count < config.MAX_EMAIL_ADDRESSES
        return ret

    def add_email(self, request, user, email, confirm=False, signup=False):
        email_object, created = self.get_or_create(
            user=user, email__iexact=email, defaults={"email": email}
        )

        if created and confirm:
            email_object.send_confirmation(request, signup=signup)

        return email_object

    def get_users_for(self, email):
        # this is a list rather than a generator because we probably want to
        # do a len() on it right away
        return [
            address.user for address in self.filter(verify=True, email__iexact=email)
        ]

    def fill_cache_for_user(self, user, addresses):
        """
        In a multi-db setup, inserting records and re-reading them later
        on may result in not being able to find newly inserted
        records. Therefore, we maintain a cache for the user so that
        we can avoid database access when we need to re-read..
        """
        user._emailaddress_cache = addresses

    def get_for_user(self, user, email):
        cache_key = "_emailaddress_cache"
        addresses = getattr(user, cache_key, None)
        if addresses is None:
            ret = self.get(user=user, email__iexact=email)
            # To avoid additional lookups when e.g.
            # EmailAddress.set_as_primary() starts touching self.user
            ret.user = user
            return ret
        else:
            for address in addresses:
                if address.email.lower() == email.lower():
                    return address
            raise self.model.DoesNotExist()


class VisitorManager(models.Manager):
    def active(self, timeout=None):
        """
        Retrieves only visitors who have been active within the timeout
        period.
        """
        if not timeout:
            timeout = utils.get_timeout()

        now = timezone.now()
        cutoff = now - timedelta(minutes=timeout)

        return self.get_query_set().filter(last_update__gte=cutoff)

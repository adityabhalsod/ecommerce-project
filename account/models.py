# Reference
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html

from __future__ import unicode_literals

import traceback
import unicodedata

from constance import config
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import check_password as django_check_password
from django.contrib.auth.hashers import is_password_usable, make_password
from django.contrib.auth.models import PermissionsMixin
from django.contrib.gis.db import models
from django.db import transaction
from django.utils import timezone
from django.utils.crypto import salted_hmac
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from account import utils
from account.choice import AddressType
from account.hmac import EmailConfirmationHMAC
from account.managers import EmailAddressManager, UserManager, VisitorManager
from base import file_dir
from base.google_map import GeoCode
from base.models import BaseModel


class AbstractBaseUser(BaseModel):
    password = models.CharField(
        _("password"), max_length=128, blank=True, null=True, default=""
    )
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)

    is_active = True

    REQUIRED_FIELDS = []

    # Stores the raw password if set_password() is called so that it can
    # be passed to password_changed() after the model is saved.
    _password = None

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_username()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def get_username(self):
        """Return the username for this User."""
        return getattr(self, self.USERNAME_FIELD)

    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

    def natural_key(self):
        return (self.get_username(),)

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return django_check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        """
        Return False if set_unusable_password() has been called for this user.
        """
        return is_password_usable(self.password)

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.password).hexdigest()

    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return "email"

    @classmethod
    def normalize_username(cls, username):
        return (
            unicodedata.normalize("NFKC", username)
            if isinstance(username, str)
            else username
        )


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("username"), max_length=30, unique=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    father_name = models.CharField(_("father name"), max_length=30, blank=True)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    last_login = models.DateTimeField(_("last login"), blank=False, auto_now_add=True)
    date_of_birth = models.DateField(_("date of birth"), blank=True, null=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=False)
    is_profile_completely_filled = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    referral_code = models.CharField(_("Referral code"), max_length=255, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        name = self.get_full_name()
        if name:
            return name
        return str(self.username)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "{} {}".format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def set_active(self):
        self.is_active = True
        return self.save()


class UserPhotos(BaseModel):
    photo = models.ImageField(
        upload_to=file_dir.profile_upload_path, blank=True, null=True
    )
    primary = models.BooleanField(default=False)
    user = models.ForeignKey(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="user_photo",
    )

    def save(self, *args, **kwargs):
        if self.primary:
            old_primary = self.__class__.objects.filter(
                user=self.user, primary=True
            ).first()
            if old_primary:
                old_primary.primary = False
                old_primary.save()
        return super(UserPhotos, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)


class UserMobileNumber(BaseModel):
    mobile_number = PhoneNumberField(
        _("mobile number"), unique=True, max_length=15, region="IN"
    )
    verify = models.BooleanField(default=False)
    primary = models.BooleanField(default=False)
    user = models.ForeignKey(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="user_mobile_number",
    )

    class Meta:
        unique_together = [("user", "mobile_number")]

    def save(self, *args, **kwargs):
        if self.primary:
            old_primary = self.__class__.objects.filter(
                user=self.user, primary=True
            ).first()
            if old_primary:
                old_primary.primary = False
                old_primary.save()
        return super(UserMobileNumber, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.mobile_number)


class UserEmail(BaseModel):
    email = models.EmailField(_("email address"), unique=True, blank=True, default="")
    verify = models.BooleanField(default=False)
    primary = models.BooleanField(default=False)
    user = models.ForeignKey(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="user_email",
    )

    objects = EmailAddressManager()

    class Meta:
        unique_together = [("user", "email")]

    def __str__(self):
        return str(self.email)

    def save(self, *args, **kwargs):
        if self.primary:
            old_primary = self.__class__.objects.filter(
                user=self.user, primary=True
            ).first()
            if old_primary:
                old_primary.primary = False
                old_primary.save()
        return super(UserEmail, self).save(*args, **kwargs)

    def set_as_primary(self, conditional=False):
        old_primary = self.__class__.objects.filter(
            user=self.user, primary=True
        ).first()
        if old_primary:
            if conditional:
                return False
            old_primary.primary = False
            old_primary.save()
        self.primary = True
        return self.save()

    def send_email_confirmation(self, request, user, signup=False, email=None):
        if email:
            try:
                email_object = self.get_for_user(user, email)
                if not email_object.verify:
                    self.send_confirmation(request, signup=signup)
            except self.DoesNotExist:
                self.__class__.objects.add_email(
                    request, user, email, signup=signup, confirm=True
                )

    def send_confirmation(self, request=None, signup=False):
        email_confirmation = EmailConfirmationHMAC(self)
        email_confirmation.confirm(request)
        return email_confirmation

    def set_verify(self):
        self.verify = True
        self.set_as_primary(conditional=True)
        self.user.set_active()
        self.save()

    def change(self, request, new_email, confirm=True):
        """
        Given a new email address, change self and re-confirm.
        """
        with transaction.atomic():
            self.email = new_email
            self.verify = False
            self.save()
            if confirm:
                self.send_confirmation(request)


class Address(BaseModel):
    address = models.TextField(null=True, blank=True)
    house_number_and_building_name = models.CharField(
        max_length=25, null=True, blank=True
    )
    street_name = models.CharField(max_length=255, null=True, blank=True)
    land_mark = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    state = models.CharField(max_length=25, null=True, blank=True)
    country = models.CharField(max_length=25, null=True, blank=True)
    pin_code = models.CharField(max_length=16, null=True, blank=True)
    address_type = models.CharField(
        max_length=255, choices=AddressType.choices, default=AddressType.HOME
    )
    notes = models.TextField(null=True, blank=True)
    geo_location = models.PointField(srid=4326, default=None, null=True, blank=True)
    primary = models.BooleanField(default=False)
    is_billing = models.BooleanField(default=False)
    is_set_manually = models.BooleanField(default=False)
    user = models.ForeignKey(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="user_address",
    )

    def __str__(self):
        return "{}, {} {}".format(
            self.address,
            self.city if self.city else "",
            self.pin_code if self.pin_code else "",
        )

    @property
    def formatted_address(self):
        address = ""

        fields = [
            self.house_number_and_building_name,
            self.street_name,
            self.land_mark,
            self.address,
        ]

        for item in fields:
            if item:
                address = address + "{}\n".format(item)

        address = address + (
            """
        {} {}
        {}
        {}
        """.format(
                self.city, self.pin_code, self.state, self.country
            )
        )

        return address

    def save(self, **kwargs):
        if not self.is_set_manually and self.geo_location and self.geo_location.coords:
            gep_code = GeoCode(coordinated=self.geo_location.coords)
            geo_coded_address = gep_code.reverse_geocode()
            if geo_coded_address:
                self.address = geo_coded_address.address
                self.city = geo_coded_address.city
                self.state = geo_coded_address.state
                self.pin_code = geo_coded_address.pin_code
                self.country = geo_coded_address.country
        if self.primary:
            old_primary = self.__class__.objects.filter(
                user=self.user, primary=True
            ).first()
            if old_primary:
                old_primary.primary = False
                old_primary.save()

        if self.is_billing:
            old_primary = self.__class__.objects.filter(
                user=self.user, is_billing=True
            ).first()
            if old_primary:
                old_primary.is_billing = False
                old_primary.save()

        super(Address, self).save(**kwargs)


class Visitor(BaseModel):
    session_key = models.CharField(max_length=40)
    ip_address = models.CharField(max_length=20)
    user = models.ForeignKey(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="user_ip_address",
    )
    user_agent = models.CharField(max_length=255)
    referrer = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    page_views = models.PositiveIntegerField(default=0)
    session_start = models.DateTimeField(default=timezone.now, editable=True)
    last_update = models.DateTimeField(default=timezone.now, editable=True)

    objects = VisitorManager()

    def __str__(self) -> str:
        return "{} - {}".format(self.user or "Anonymous", self.ip_address)

    @property
    def time_on_site(self):
        """
        Attempts to determine the amount of time a visitor has spent on the
        site based upon their information that's in the database.
        """
        if self.session_start:
            seconds = (self.last_update - self.session_start).seconds

            hours = seconds / 3600
            seconds -= hours * 3600
            minutes = seconds / 60
            seconds -= minutes * 60

            return "%i:%02i:%02i" % (hours, minutes, seconds)
        else:
            return "unknown"

    @property
    def geoip_data(self):
        """
        Attempts to retrieve MaxMind GeoIP data based upon the visitor's IP
        """
        from django.contrib.gis.geoip2 import GeoIP2, GeoIP2Exception

        CACHE_TYPE = config.GEOIP_CACHE_TYPE

        if not hasattr(self, "_geoip_data"):
            self._geoip_data = None
            try:
                gip = GeoIP2(cache=CACHE_TYPE)
                self._geoip_data = gip.city(self.ip_address)
            except GeoIP2Exception:
                # don't even bother...
                print(
                    'Error getting GeoIP data for IP "%s": %s'
                    % (self.ip_address, traceback.format_exc())
                )

        return self._geoip_data

    @property
    def geoip_data_json(self):
        """
        Cleans out any dirty unicode characters to make the geoip data safe for
        JSON encoding.
        """
        clean = {}
        if not self.geoip_data:
            return {}

        for key, value in self.geoip_data.items():
            clean[key] = utils.u_clean(value)
        return clean

    class Meta:
        ordering = ("-last_update",)


class UntrackedUserAgent(BaseModel):
    keyword = models.CharField(
        _("keyword"),
        max_length=100,
        help_text=_(
            'Part or all of a user-agent string.  For example, "Googlebot" here will be found in "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" and that visitor will not be tracked.'
        ),
    )

    def __str__(self):
        return str(self.keyword)

    class Meta:
        ordering = ("keyword",)
        verbose_name = _("Untracked User-Agent")
        verbose_name_plural = _("Untracked User-Agents")


class BannedIP(BaseModel):
    ip_address = models.GenericIPAddressField(
        "IP Address", help_text=_("The IP address that should be banned")
    )

    def __str__(self):
        return str(self.ip_address)

    class Meta:
        ordering = ("ip_address",)
        verbose_name = _("Banned IP")
        verbose_name_plural = _("Banned IPs")

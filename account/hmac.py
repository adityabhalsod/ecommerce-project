from constance import config
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing

from account.tasks import send_mail
from v1.emailtemplate.choice import EmailTemplateChoices


class EmailConfirmationHMAC:
    def __init__(self, email_object=None):
        self.email_object = email_object

    @property
    def key(self):
        return signing.dumps(obj=self.email_object.pk, salt=settings.SECRET_KEY)

    @classmethod
    def from_key(cls, key):
        from account.models import UserEmail

        try:
            max_age = 60 * 60 * 24 * config.EMAIL_CONFIRMATION_EXPIRE_DAYS
            pk = signing.loads(key, max_age=max_age, salt=settings.SECRET_KEY)
            ret = EmailConfirmationHMAC(UserEmail.objects.get(pk=pk))
        except (
            signing.SignatureExpired,
            signing.BadSignature,
            UserEmail.DoesNotExist,
        ):
            ret = None
        return ret

    def set_verify(self):
        self.email_object.set_verify()
        return self.email_object

    def confirm(self, request):
        email_object = self.email_object
        if not email_object.verify:
            self.send(request, type=EmailTemplateChoices.CONFIRMATION)
        return email_object

    def forgot_password(self, request):
        self.send(request, type=EmailTemplateChoices.FORGOT_PASSWORD)
        return self.email_object

    def reset_password(self, request):
        self.send(request, type=EmailTemplateChoices.RESET_PASSWORD)
        return self.email_object

    def change_password(self, request):
        self.send(request, type=EmailTemplateChoices.CHANGE_PASSWORD)
        return self.email_object

    def account_deactivate(self, request):
        self.send(request, type=EmailTemplateChoices.ACCOUNT_DEACTIVATE)
        return self.email_object

    def send(self, request=None, type=None):
        activate_url = config.EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL
        context = {
            "user": self.email_object.user,
            "activate_url": activate_url,
            "current_site": get_current_site(request),
            "key": self.key,
        }
        send_mail.delay(to=self.email_object.email, type=type, context=context)
        return True

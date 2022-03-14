import sendgrid
from constance import config as constance_config
from django.template import Context, Template
from sendgrid.helpers import mail

from v1.emailtemplate.models import EmailTemplate


class MailClient(object):
    def __init__(self, SENDGRID_KEY=""):
        """
        Init for mail client.
        """
        self.sendgrid = sendgrid.SendGridAPIClient(SENDGRID_KEY)

    def send(self, to_email, type, context={}):
        """
        Configuration for sending mail to and subject.

        @parmas : form_email (string) : Email ID for mail sender.
        @parmas : to_email (string or python list) : Email ID for mail receiver.
        @parmas : subject (string) : Email subject.
        """

        try:
            email_template = EmailTemplate.objects.get(title=type)
        except EmailTemplate.DoesNotExist:
            raise ValueError(
                "Email template are not found.",
                format(str(self.__class__.__name__)),
            )

        content = Template(email_template.html_content)

        if not content:
            raise ValueError(
                "Email content are not found!.",
                format(str(self.__class__.__name__)),
            )

        mail_content = mail.Mail(
            from_email=constance_config.DEFAULT_FROM_EMAIL,
            to_emails=[str(to_email)],
            subject=email_template.subject,
            html_content=content.render(Context(context)),
        )

        self.sendgrid.send(mail_content)

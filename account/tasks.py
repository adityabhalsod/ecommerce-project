from constance import config

from config.celery import app
from service.msg91_otp import OTPClient
from service.sendgrid.client import MailClient


def default_kwargs():
    kwargs = {}
    if config.OTP_EXPIRY_TIME:
        kwargs["otp_expiry"] = config.OTP_EXPIRY_TIME
    if config.OTP_LENGTH:
        kwargs["otp_length"] = config.OTP_LENGTH
    return kwargs


@app.task
def send_otp(mobile_number):
    MSG_91_AUTH_KEY = config.MSG_91_AUTH_KEY
    otp_client = OTPClient(auth_key=MSG_91_AUTH_KEY)
    kwargs = default_kwargs()
    respone = otp_client.send_otp(mobile_number=mobile_number, **kwargs)
    print(respone, "------------------------send-otp")


@app.task
def resend_otp(mobile_number, retry_type):
    MSG_91_AUTH_KEY = config.MSG_91_AUTH_KEY
    otp_client = OTPClient(auth_key=MSG_91_AUTH_KEY)
    kwargs = default_kwargs()
    return otp_client.resend_otp(
        mobile_number=mobile_number, retry_type=retry_type, **kwargs
    )


@app.task
def verify_otp(mobile_number, otp_value):
    MSG_91_AUTH_KEY = config.MSG_91_AUTH_KEY
    otp_client = OTPClient(auth_key=MSG_91_AUTH_KEY)
    kwargs = default_kwargs()
    return otp_client.verify_otp(
        mobile_number=mobile_number, otp_value=otp_value, **kwargs
    )


@app.task
def send_mail(to, type, context):
    if not type:
        print("Type are not found!")
        return False

    client = MailClient(config.SEND_GRID_API_KEY)
    client.send(to, type, context)
    print("------------------------send-mail")

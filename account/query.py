from account.models import UserEmail, UserMobileNumber


def get_user_email(user):
    instance = UserEmail.objects.filter(user=user, primary=True).first()
    return str(instance.email)


def get_user_mobile_number(user):
    instance = UserMobileNumber.objects.filter(user=user, primary=True).first()
    return str(instance.mobile_number)

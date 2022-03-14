import re
import unicodedata
from django.apps import apps
from django.conf import settings

# this is not intended to be an all-knowing IP address regex
IP_RE = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
EMAIL_REGEX = re.compile(
    r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
)


def email_is_valid(email):
    if re.fullmatch(EMAIL_REGEX, email):
        return True
    else:
        return False


def get_timeout():
    """
    Gets any specified timeout from the settings file, or use 10 minutes by
    default
    """
    return getattr(settings, "TRACKING_TIMEOUT", 10)


def get_cleanup_timeout():
    """
    Gets any specified visitor clean-up timeout from the settings file, or
    use 24 hours by default
    """
    return getattr(settings, "TRACKING_CLEANUP_TIMEOUT", 24)


def u_clean(s):
    """A strange attempt at cleaning up unicode"""

    uni = ""
    try:
        # try this first
        uni = str(s)
    except UnicodeDecodeError:
        try:
            # try utf-8 next
            uni = str(s).decode("utf-8")
        except UnicodeDecodeError:
            # last resort method... one character at a time (ugh)
            if s and type(s) in (str):
                for c in s:
                    try:
                        uni += unicodedata.normalize("NFKC", str(c))
                    except UnicodeDecodeError:
                        uni += "-"

    return uni.encode("ascii", "xmlcharrefreplace")


def get_projects_apps_models():
    list_of_models = []
    for app in apps.get_app_configs():
        if app.label in settings.PROJECT_APPS:
            list_of_models.append(str(app.label))
    return list_of_models

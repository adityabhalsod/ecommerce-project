from django.contrib.gis.db import models


class EmailTemplateChoices(models.TextChoices):
    FORGOT_PASSWORD = "forgot_password", "Forgot Password"
    RESET_PASSWORD = "reset_password", "Reset password"
    CONFIRMATION = "confirmation", "Confirmation Email"
    CHANGE_PASSWORD = "change_password", "Change password"
    ACCOUNT_DEACTIVATE = "account_deactivate", "Account Deactivate"

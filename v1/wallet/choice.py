from django.contrib.gis.db import models


class WalletType(models.TextChoices):
    CUSTOMER = "customer", "Customer"
    DELIVERY_BOY = "delivery_boy", "Delivery Boy"
    NOT_ATTEMPT = "not_attempt", "Not attempt"


class TransactionType(models.TextChoices):
    PAYMENT = "payment", "Payment"
    REFUND = "refund", "Refund"
    ADD_MONEY_IN_WALLET = "add_money_in_wallet", "Add money in wallet"
    ADD_MEMBERSHIP = "add_membership", "Add membership"
    CASHBACK = "cashback", "Cashback"
    NOT_ATTEMPT = "not_attempt", "Not attempt"


class TransactionMethod(models.TextChoices):
    CREDIT = "credit", "Credit (+)"
    DEBIT = "debit", "Debit (-)"
    NOT_ATTEMPT = "not_attempt", "Not attempt"


class TransactionStatus(models.TextChoices):
    WATING = "wating", "Wating"
    SUCCESSFUL = "successful", "Successful"
    FAILED = "failed", "Failed"
    NOT_ATTEMPT = "not_attempt", "Not attempt"


class TransactionPlatform(models.TextChoices):
    QR_CODE = "qr_code", "QR Code"
    WALLET = "wallet", "Wallet"
    ONLINE = "online", "Online"
    CASH = "cash", "Cash"
    NOT_ATTEMPT = "not_attempt", "Not attempt"

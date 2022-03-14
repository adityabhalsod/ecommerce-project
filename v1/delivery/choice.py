from django.contrib.gis.db import models


class DeliveryBoyStatus(models.TextChoices):
    OFFLINE = "offline", "Offline"
    ONLINE = "online", "Online"
    READY_FOR_ORDER_PICKED_UP = "ready_for_order_picked_up", "Ready for order picked up"
    ORDER_PICKED_UP = "order_picked_up", "Order picked up"
    DELIVERY_ON_THE_WAY = "delivery_on_the_way", "Delivery on the way"


class DeliveryBoyVehicleType(models.TextChoices):
    AUTO_RICKSHAW = "auto_rickshaw", "Auto-rickshaw"
    CYCLE = "cycle", "Cycle"
    MOTOR_CYCLE = "motor_cycle", "Motor cycle"
    MINI_TRUCK = "mini_truck", "Mini truck"
    OTHER = "other", "Other"
    TRUCK = "truck", "Truck"


class DeliveryBoyDocumentType(models.TextChoices):
    AADHAR_CARD = "aadhar_card", "Aadhar card"
    ADDRESS_PROOF = "address_proof", "Address proof"
    BANK_ACCOUNT_PASSBOOK = "bank_account_passbook", "Bank account passbook"
    DRIVING_LICENSE = "driving_license", "Driving license"
    OTHER = "other", "Other"
    PAN_CARD = "pan_card", "Pan card"
    VOTER_ID = "voter_id", "Voter ID"


class DeliveryBoyReviewChoice(models.TextChoices):
    VERYBAD = 1, "Very bad"
    BAD = 2, "Bad"
    OKAY = 3, "Okay"
    GOOD = 4, "Good"
    EXCELLENT = 5, "Excellent"


class Status(models.TextChoices):
    APPROVE = "approve", "Approve"
    REJECT = "reject", "Reject"
    PENDING = "pending", "Pending"

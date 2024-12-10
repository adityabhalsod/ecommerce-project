import os
from io import BytesIO

from django.contrib.gis.db import models
from django.core.files.base import ContentFile
from PIL import Image
from base import file_dir
from base.models import BaseModel
from v1.delivery.choice import (
    DeliveryBoyDocumentType,
    DeliveryBoyReviewChoice,
    DeliveryBoyStatus,
    DeliveryBoyVehicleType,
    Status,
)


class DeliveryBoy(BaseModel):
    user = models.ForeignKey(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="delivery_boy_user",
    )
    store = models.ForeignKey(
        "store.Store",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="delivery_boy_store",
    )
    payout_balance = models.FloatField(default=0.0, null=True, blank=True)
    current_status = models.CharField(
        max_length=255,
        choices=DeliveryBoyStatus.choices,
        default=DeliveryBoyStatus.OFFLINE,
    )
    status = models.CharField(
        max_length=255,
        choices=Status.choices,
        default=Status.PENDING,
    )
    bank_account_ifsc_code = models.CharField(max_length=50, default="")
    bank_account_number = models.CharField(max_length=50, default="")
    bank_account_name = models.CharField(
        max_length=50, default="", null=True, blank=True
    )
    bank_name = models.CharField(max_length=50, default="", null=True, blank=True)
    bank_branch_name = models.CharField(
        max_length=50, default="", null=True, blank=True
    )
    bank_branch_address = models.TextField(default="", null=True, blank=True)

    class Meta:
        app_label = "delivery"
        unique_together = [("user",)]

    def __str__(self):
        return str(self.user)


class DeliveryBoyVehiclePhotos(BaseModel):
    class Meta:
        app_label = "delivery"
        
    original = models.ImageField(
        upload_to=file_dir.delivery_boy_vehicle_original_upload_path,
        blank=True,
        null=True,
    )
    webp_image = models.ImageField(
        upload_to=file_dir.delivery_boy_vehicle_webp_upload_path, blank=True, null=True
    )
    thumbnail = models.ImageField(
        upload_to=file_dir.delivery_boy_vehicle_thumbnail_upload_path,
        blank=True,
        null=True,
    )
    alt_text = models.TextField(default="")

    def save(self, *args, **kwargs):
        MAX_SIZE = (500, 500)
        if self.original and str(self.original).split(".")[-1] != "svg":
            filename = os.path.splitext(str(self.original))
            file_tuple = list(filename)
            new_file_webp = str(file_tuple[0] + ".webp")
            new_file_thumbnail = str(file_tuple[0] + file_tuple[1])
            image = Image.open(self.original)

            web_image_io = BytesIO()
            image.save(web_image_io, format="WEBP", quality=90)
            self.webp_image.save(
                new_file_webp, ContentFile(web_image_io.getvalue()), save=False
            )

            thumbnail_image_io = BytesIO()
            image.thumbnail(MAX_SIZE)
            image.save(thumbnail_image_io, format="PNG", quality=50)
            self.thumbnail.save(
                new_file_thumbnail,
                ContentFile(thumbnail_image_io.getvalue()),
                save=False,
            )

        return super(DeliveryBoyVehiclePhotos, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.alt_text) if self.alt_text else str(self.pk)


class DeliveryBoyVehicleInformation(BaseModel):
    delivery_boy = models.ForeignKey(
        "delivery.DeliveryBoy",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="vehicle_information",
    )
    vehicle_type = models.CharField(
        max_length=255,
        choices=DeliveryBoyVehicleType.choices,
        default=DeliveryBoyVehicleType.MOTOR_CYCLE,
    )
    vehicle_number = models.CharField(max_length=255, default="", null=True, blank=True)
    status = models.CharField(
        max_length=255,
        choices=Status.choices,
        default=Status.PENDING,
    )
    photos = models.ManyToManyField(
        "delivery.DeliveryBoyVehiclePhotos",
        related_name="delivery_boy_vehicle_photos",
        blank=True,
    )

    def __str__(self):
        return str(self.delivery_boy.user) if self.delivery_boy else "N/A"


class DeliveryBoyDocument(BaseModel):
    delivery_boy = models.ForeignKey(
        "delivery.DeliveryBoy",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="delivery_boy_vehicle_information",
    )
    document_id_number = models.CharField(
        max_length=255, default="", null=True, blank=True
    )
    document_type = models.CharField(
        max_length=255,
        choices=DeliveryBoyDocumentType.choices,
        default=DeliveryBoyDocumentType.AADHAR_CARD,
    )
    front = models.ImageField(
        upload_to=file_dir.delivery_boy_document_front,
        blank=True,
        null=True,
    )
    back = models.ImageField(
        upload_to=file_dir.delivery_boy_document_back,
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=255,
        choices=Status.choices,
        default=Status.PENDING,
    )

    def __str__(self):
        return str(self.delivery_boy.user) if self.delivery_boy else "N/A"


class DeliveryBoyReview(BaseModel):
    delivery_boy = models.ForeignKey(
        "delivery.DeliveryBoy",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="delivery_boy_review",
    )
    author = models.ForeignKey(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="delivery_review_user",
    )

    title = models.CharField(max_length=255, default="", null=True, blank=True)
    text = models.TextField(default="")
    rating = models.CharField(
        max_length=5,
        choices=DeliveryBoyReviewChoice.choices,
        default=DeliveryBoyReviewChoice.OKAY,
    )

    def __str__(self):
        return str(self.delivery_boy.user) if self.delivery_boy else "N/A"

    # TODO: Implemented logic
    @property
    def average(self):
        raise NotImplemented


class DeliveryBoyPayoutInformation(BaseModel):
    delivery_boy = models.ForeignKey(
        "delivery.DeliveryBoy",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="delivery_boy_payout_account",
    )
    bank_account_ifsc_code = models.CharField(max_length=50)
    bank_account_number = models.CharField(max_length=50)
    bank_account_name = models.CharField(
        max_length=50, default="", null=True, blank=True
    )
    bank_name = models.CharField(max_length=50, default="", null=True, blank=True)
    bank_branch_name = models.CharField(
        max_length=50, default="", null=True, blank=True
    )
    bank_account_proof = models.ImageField(
        upload_to=file_dir.delivery_boy_bank_account_proof_upload_path,
        null=True,
        blank=True,
    )
    bank_branch_address = models.TextField(default="", null=True, blank=True)
    payout_balance = models.FloatField(default=0.0, null=True, blank=True)

    def __str__(self):
        return str(self.delivery_boy.user) if self.delivery_boy else "N/A"


class DeliveryCharges(BaseModel):
    title = models.CharField(max_length=255, default="", null=True, blank=True)
    amount_starting_range = models.FloatField(default=0.0)
    amount_ending_range = models.FloatField(default=0.0)
    delivery_charge = models.FloatField(default=0.0, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

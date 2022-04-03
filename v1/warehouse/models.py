from django.contrib.gis.db import models
from django.utils import timezone
from base import file_dir
from base.models import BaseModel
from v1.warehouse.choice import ProductTaxType, DiscountType
from v1.warehouse.tasks import stock_purchase, stock_transfer


class Warehouse(BaseModel):
    name = models.CharField(max_length=255, default="", null=True, blank=True)
    city = models.CharField(max_length=64, default="", null=True, blank=True)
    state = models.CharField(max_length=25, default="", null=True, blank=True)
    country = models.CharField(max_length=25, default="", null=True, blank=True)
    pin_code = models.CharField(max_length=16, default="", null=True, blank=True)
    address = models.TextField(default="", null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


class Supplier(BaseModel):
    business_name = models.CharField(max_length=255, default="", null=True, blank=True)
    mobile = models.CharField(max_length=255, default="", null=True, blank=True)
    email = models.CharField(max_length=255, default="", null=True, blank=True)
    gst_number = models.CharField(max_length=255, default="", null=True, blank=True)
    address = models.TextField(default="", null=True, blank=True)
    city = models.CharField(max_length=64, default="", null=True, blank=True)
    state = models.CharField(max_length=25, default="", null=True, blank=True)
    country = models.CharField(max_length=25, default="", null=True, blank=True)
    pin_code = models.CharField(max_length=16, default="", null=True, blank=True)

    def __str__(self):
        return str(self.business_name)


class Purchase(BaseModel):
    multiple_item = models.ManyToManyField(
        "warehouse.PurchaseMultiItem", related_name="purchase_multipleitem", blank=True
    )
    item_supplier = models.ForeignKey(
        "warehouse.Supplier", null=True, blank=True, on_delete=models.CASCADE
    )
    reference_number = models.CharField(
        max_length=255, default="", null=True, blank=True
    )
    datetime = models.DateTimeField(default=timezone.now)
    warehouse = models.ForeignKey(
        "warehouse.Warehouse",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    attach_document = models.FileField(
        upload_to=file_dir.purchase_attach_document,
        blank=True,
        null=True,
    )
    additional_shipping_charges = models.FloatField(default=0.0, null=True, blank=True)
    additional_notes = models.TextField(default="", null=True, blank=True)
    discount_type = models.CharField(
        max_length=10,
        choices=DiscountType.choices,
        default=DiscountType.FIXED,
    )
    tax = models.CharField(
        default=ProductTaxType.NOT_ATTEMPT,
        max_length=5,
        null=True,
        blank=True,
        choices=ProductTaxType.choices,
    )
    discount = models.FloatField(default=0.0, null=True, blank=True)

    # auto calculation
    total_items = models.IntegerField(default=0, null=True, blank=True)
    sub_total = models.FloatField(default=0.0, null=True, blank=True)
    purchase_total = models.FloatField(default=0.0, null=True, blank=True)

    def __str__(self):
        return str(self.reference_number) if self.reference_number else str(self.pk)


#  MultipleItem for Purchase
class PurchaseMultiItem(BaseModel):
    product_and_variation = models.ForeignKey(
        "catalog.Variation",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="purchase_product_and_variation",
    )
    quantity = models.BigIntegerField(default=0)
    unit_cost = models.FloatField(default=0.0, null=True, blank=True)
    price = models.FloatField(default=0.0, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.quantity and self.unit_cost:
            self.price = float(self.quantity) * float(self.unit_cost)
        else:
            self.price = 0.0

        return super(PurchaseMultiItem, self).save(*args, **kwargs)

    def __str__(self):
        return (
            str(self.product_and_variation) + " x " + str(self.quantity)
            if self.product_and_variation
            else str(self.pk) + " x " + str(self.quantity)
        )


class StockTransfer(BaseModel):
    multiple_item = models.ManyToManyField(
        "warehouse.StockTransferMultiItem",
        related_name="stocktransfer_multipleitem",
        blank=True,
    )
    datetime = models.DateTimeField(default=timezone.now)
    warehouse = models.ForeignKey(
        "warehouse.Warehouse",
        null=True,
        blank=True,
        help_text="From warehouse",
        on_delete=models.CASCADE,
    )
    store = models.ForeignKey(
        "store.Store",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="To Store",
    )
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pk)


class StockTransferMultiItem(BaseModel):
    product_and_variation = models.ForeignKey(
        "catalog.Variation",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="stock_transfer_product_and_variation",
    )
    quantity = models.BigIntegerField(default=0)

    def __str__(self):
        return (
            str(self.product_and_variation) + " x " + str(self.quantity)
            if self.product_and_variation
            else str(self.pk) + " x " + str(self.quantity)
        )


class WarehouseStockManagement(BaseModel):
    product_and_variation = models.ForeignKey(
        "catalog.Variation",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    warehouse = models.ForeignKey(
        "warehouse.Warehouse",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    purchase_reference = models.ForeignKey(
        "warehouse.Purchase",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    quantity = models.BigIntegerField(default=0)
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.pk)


class StoreStockManagement(BaseModel):
    product_and_variation = models.ForeignKey(
        "catalog.Variation",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    store = models.ForeignKey(
        "store.Store",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    transfer_reference = models.ForeignKey(
        "warehouse.StockTransfer",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    quantity = models.BigIntegerField(default=0)
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.pk)

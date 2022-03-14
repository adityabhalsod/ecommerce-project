import os
from io import BytesIO

from django.contrib.gis.db import models
from django.core.files.base import ContentFile
from django.db.models import Max
from django.template.defaultfilters import slugify
from django.utils.encoding import force_text
from PIL import Image

from base import file_dir
from base.models import BaseModel
from v1.catalog.choice import ProductTaxType, ProductType


class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    parent_category = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="children"
    )
    sequence = models.BigIntegerField(default=0, null=True, blank=True)
    slug = models.CharField(default="", max_length=255, blank=True, null=True)
    image = models.ImageField(
        upload_to=file_dir.category_upload_path, blank=True, null=True
    )
    webp_image = models.ImageField(
        upload_to=file_dir.category_webp_upload_path, blank=True, null=True
    )
    thumbnail = models.ImageField(
        upload_to=file_dir.category_thumbnail_upload_path,
        blank=True,
        null=True,
    )
    description = models.TextField(default="")
    background_color = models.CharField(
        default="", max_length=255, blank=True, null=True
    )
    is_main = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        MAX_SIZE = (500, 500)
        if self.image and str(self.image).split(".")[-1] != "svg":
            filename = os.path.splitext(str(self.image))
            file_tuple = list(filename)
            new_file_webp = str(file_tuple[0] + ".webp")
            new_file_thumbnail = str(file_tuple[0] + file_tuple[1])
            image = Image.open(self.image)

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

        # slugify
        self.slug = slugify(force_text(self.name))

        if self._state.adding:
            # Current count
            current_count = (
                self.__class__.objects.aggregate(Max("sequence")).get("sequence__max")
                or 0
            )

            # sequence
            self.sequence = current_count + 1

        # Not able to set the parent category as a this category.
        if self.parent_category and self.parent_category.pk == self.pk:
            self.parent_category = None

        # Not able to set the recursive category.
        if (
            self.parent_category
            and self.parent_category.parent_category
            and self.parent_category.parent_category.pk == self.pk
        ):
            self.parent_category = None

        # auto sub category.
        if self.parent_category:
            self.is_main = False

        return super(Category, self).save(*args, **kwargs)


class Unit(BaseModel):
    name = models.CharField(max_length=50, default="", null=True, blank=True)
    short_name = models.CharField(max_length=10, default="", null=True, blank=True)

    def __str__(self):
        return str(self.name) + " | " + str(self.short_name)


class ProductPhoto(BaseModel):
    original = models.ImageField(
        upload_to=file_dir.product_upload_path, blank=True, null=True
    )
    webp_image = models.ImageField(
        upload_to=file_dir.product_webp_upload_path, blank=True, null=True
    )
    thumbnail = models.ImageField(
        upload_to=file_dir.product_thumbnail_upload_path, blank=True, null=True
    )
    alt_text = models.TextField(default="")
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return str(self.alt_text) if self.alt_text else str(self.pk)

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

        return super(ProductPhoto, self).save(*args, **kwargs)


class Product(BaseModel):
    item_code = models.CharField(max_length=255, default="", null=True, blank=True)
    item_name = models.CharField(max_length=255, default="", null=True, blank=True)
    bill_display_item_name = models.CharField(
        max_length=255, default="", null=True, blank=True
    )
    short_description = models.TextField(default="", null=True, blank=True)
    search_keyword = models.TextField(default="")
    slug = models.CharField(default="", max_length=255, blank=True, null=True)

    category = models.ForeignKey(
        "catalog.Category",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="product_category",
    )
    photos = models.ManyToManyField(
        "catalog.ProductPhoto", related_name="product_photos", blank=True
    )
    tax = models.CharField(
        default=ProductTaxType.NOT_ATTEMPT,
        max_length=5,
        null=True,
        blank=True,
        choices=ProductTaxType.choices,
    )

    def __str__(self):
        return str(self.item_name)

    def save(self, *args, **kwargs):
        self.slug = slugify(force_text(self.item_name))
        return super(Product, self).save(*args, **kwargs)


class ProductStockMaster(BaseModel):
    is_exclusive_item = models.BooleanField(default=False)
    is_super_saving_item = models.BooleanField(default=False)
    one_rs_store = models.BooleanField(default=False)
    is_active_item = models.BooleanField(default=False)
    type = models.CharField(
        max_length=255, choices=ProductType.choices, default=ProductType.SINGLE
    )
    store = models.ManyToManyField(
        "store.Store", blank=True, related_name="store_product_stock_master"
    )
    product = models.ForeignKey(
        "catalog.Product", null=True, blank=True, on_delete=models.CASCADE
    )
    position = models.CharField(max_length=255, default="", null=True, blank=True)
    row = models.CharField(max_length=255, default="", null=True, blank=True)
    rack = models.CharField(max_length=255, default="", null=True, blank=True)

    def __str__(self):
        return str(self.product)


class VariationPhoto(BaseModel):
    original = models.ImageField(
        upload_to=file_dir.variation_upload_path, blank=True, null=True
    )
    webp_image = models.ImageField(
        upload_to=file_dir.variation_webp_upload_path, blank=True, null=True
    )
    thumbnail = models.ImageField(
        upload_to=file_dir.variation_thumbnail_upload_path, blank=True, null=True
    )
    alt_text = models.TextField(default="")
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return str(self.alt_text) if self.alt_text else str(self.pk)

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

        return super(VariationPhoto, self).save(*args, **kwargs)


class Variation(BaseModel):
    product_stock_master = models.ForeignKey(
        "catalog.ProductStockMaster",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="stock_master_variation",
    )
    photos = models.ManyToManyField(
        "catalog.VariationPhoto", related_name="variation_photos", blank=True
    )
    name = models.CharField(
        max_length=255,
        default="",
    )
    value = models.IntegerField(default=0)
    unit = models.ForeignKey(
        "catalog.Unit",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="variantion_unit",
    )
    upc_barcode = models.CharField(
        verbose_name="Universal Product Code",
        max_length=255,
        default="",
        null=True,
        blank=True,
    )
    hsn_code = models.CharField(max_length=255, default="", null=True, blank=True)
    mrp = models.FloatField(default=0.0, null=True, blank=True)
    our_rate = models.FloatField(default=0.0, null=True, blank=True)
    member_rate = models.FloatField(default=0.0, null=True, blank=True)
    exclusive_rate = models.FloatField(default=0.0, null=True, blank=True)
    purchase_rate = models.FloatField(default=0.0, null=True, blank=True)
    max_order_quantity = models.IntegerField(default=0)
    min_stock = models.IntegerField(verbose_name="Alert quantity", default=0)
    open_stock = models.IntegerField(verbose_name="Open stock", default=0)

    def __str__(self):
        return str(self.name) if self.name else str(self.pk)

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.our_rate:
                self.our_rate = self.mrp
            if not self.member_rate:
                if self.our_rate:
                    self.member_rate = self.our_rate
                else:
                    self.member_rate = self.mrp
            if not self.exclusive_rate:
                if self.our_rate:
                    self.exclusive_rate = self.our_rate
                else:
                    self.exclusive_rate = self.mrp
        return super(Variation, self).save(*args, **kwargs)

    @property
    def our_rate_difference(self):
        if self.mrp and self.our_rate:
            return self.mrp - self.our_rate
        return 0.0

    @property
    def member_rate_difference(self):
        if self.mrp and self.member_rate:
            return self.mrp - self.member_rate
        return 0.0

    @property
    def exclusive_rate_difference(self):
        if self.mrp and self.exclusive_rate:
            return self.mrp - self.exclusive_rate
        return 0.0

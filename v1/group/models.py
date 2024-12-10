import os
from django.contrib.gis.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import force_str
from base.models import BaseModel
from django.db.models import Max
from base import file_dir
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from v1.group.choice import Alignment, Level


class GroupType(BaseModel):
    type = models.CharField(max_length=255, default="")
    display = models.CharField(max_length=255, default="")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.display) if self.display else str(self.type)


class Color(BaseModel):
    name = models.CharField(max_length=255, default="")
    image = models.ImageField(upload_to=file_dir.group_color, blank=True, null=True)
    key = models.CharField(max_length=255, default="")

    def __str__(self):
        return str(self.name)


class MultiplePhotos(BaseModel):
    original = models.ImageField(
        upload_to=file_dir.group_multiphotos_upload_path, blank=True, null=True
    )
    webp_image = models.ImageField(
        upload_to=file_dir.group_multiphotos_webp_upload_path, blank=True, null=True
    )
    thumbnail = models.ImageField(
        upload_to=file_dir.group_multiphotos_thumbnail_upload_path,
        blank=True,
        null=True,
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
        return super(MultiplePhotos, self).save(*args, **kwargs)


class GroupStructure(BaseModel):
    store = models.ManyToManyField(
        "store.Store", blank=True, related_name="store_group"
    )
    group_name = models.CharField(max_length=255, default="")
    sequence = models.BigIntegerField(default=0, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    parent_group = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="children"
    )
    background_color = models.ForeignKey(
        "group.Color",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="group_background_color",
    )
    bottem_line_color = models.ForeignKey(
        "group.Color",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="group_bottem_line_color",
    )
    level = models.CharField(
        max_length=10, choices=Level.choices, default=Level.ONE, null=True, blank=True
    )
    self_identify = models.ForeignKey(
        "group.GroupType",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    short_text = models.CharField(max_length=255, default="")
    long_text = models.TextField(default="")
    redirection_key = models.TextField(default="")
    image = models.ImageField(
        upload_to=file_dir.group_upload_path, blank=True, null=True
    )
    webp_image = models.ImageField(
        upload_to=file_dir.group_webp_upload_path, blank=True, null=True
    )
    thumbnail = models.ImageField(
        upload_to=file_dir.group_thumbnail_upload_path,
        blank=True,
        null=True,
    )
    multiple_photos = models.ManyToManyField(
        "group.MultiplePhotos", related_name="group_multiple_photos", blank=True
    )
    is_main = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Group Structure"
        verbose_name_plural = "Group Structures"

    def __str__(self):
        return str(self.group_name)

    def save(self, *args, **kwargs):
        # slugify
        self.slug = slugify(force_str(self.group_name))

        if self._state.adding:
            # Current count
            current_count = (
                self.__class__.objects.aggregate(Max("sequence")).get("sequence__max")
                or 0
            )

            # sequence
            self.sequence = current_count + 1

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

        # auto set is main true or false.
        if self.parent_group:
            self.is_main = False

        return super(GroupStructure, self).save(*args, **kwargs)


class Collection(BaseModel):
    alignment = models.CharField(
        max_length=10,
        choices=Alignment.choices,
        default=Alignment.HORIZONTAL,
        null=True,
        blank=True,
    )
    group = models.ForeignKey(
        "group.GroupStructure",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="group_collection",
    )
    sequence = models.BigIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.group.group_name) if self.group.group_name else "N/A"

    def save(self, *args, **kwargs):
        if self._state.adding:
            # Current count
            current_count = (
                self.__class__.objects.aggregate(Max("sequence")).get("sequence__max")
                or 0
            )

            # sequence
            self.sequence = current_count + 1

        if self.group and self.group.level != Level.TWO:
            self.group.level = Level.TWO
            self.group.save()

        return super(Collection, self).save(*args, **kwargs)


class ProductCollection(BaseModel):
    store = models.ForeignKey(
        "store.Store",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="store_product_collection",
    )
    product = models.ForeignKey(
        "catalog.Product",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    collection = models.ForeignKey(
        "group.Collection", null=True, blank=True, on_delete=models.CASCADE
    )
    sequence = models.BigIntegerField(default=0, null=True, blank=True)
    background_color = models.ForeignKey(
        "group.Color",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="background_color",
    )
    bottem_line_color = models.ForeignKey(
        "group.Color",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="bottem_line_color",
    )

    def save(self, *args, **kwargs):
        if self._state.adding:
            # Current count
            current_count = (
                self.__class__.objects.aggregate(Max("sequence")).get("sequence__max")
                or 0
            )

            # sequence
            self.sequence = current_count + 1

        return super(ProductCollection, self).save(*args, **kwargs)

    def __str__(self):
        if self.product and self.product.item_name:
            return str(self.product.item_name)
        return "N/A"

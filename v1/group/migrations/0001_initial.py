# Generated by Django 3.0.8 on 2022-01-21 19:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import base.file_dir


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("store", "0004_auto_20220116_1913"),
        ("catalog", "0026_product_tax"),
    ]

    operations = [
        migrations.CreateModel(
            name="Collection",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "alignment",
                    models.SmallIntegerField(
                        blank=True,
                        choices=[("1", "Horizontal"), ("2", "Vertical")],
                        default="1",
                        null=True,
                    ),
                ),
                ("sequence", models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Color",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_deleted", models.BooleanField(default=False)),
                ("name", models.CharField(default="", max_length=255)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to=base.file_dir.group_color
                    ),
                ),
                ("key", models.CharField(default="", max_length=255)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="GroupType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_deleted", models.BooleanField(default=False)),
                ("type", models.CharField(default="", max_length=255)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProductCollection",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_deleted", models.BooleanField(default=False)),
                ("sequence", models.IntegerField(blank=True, default=0, null=True)),
                (
                    "background",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="background_color",
                        to="group.Color",
                    ),
                ),
                (
                    "bottem_line",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bottem_line_color",
                        to="group.Color",
                    ),
                ),
                (
                    "collection",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="group.Collection",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.Product",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="GroupStructure",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_deleted", models.BooleanField(default=False)),
                ("group_name", models.CharField(default="", max_length=255)),
                ("sequence", models.IntegerField(blank=True, default=0, null=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "level",
                    models.SmallIntegerField(
                        blank=True,
                        choices=[("1", "Level 1"), ("2", "Level 2"), ("3", "Level 3")],
                        default="1",
                        null=True,
                    ),
                ),
                ("short_text", models.CharField(default="", max_length=255)),
                ("long_text", models.TextField(default="")),
                ("redirection_key", models.TextField(default="")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=base.file_dir.group_upload_path,
                    ),
                ),
                (
                    "webp_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=base.file_dir.group_webp_upload_path,
                    ),
                ),
                (
                    "thumbnail",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=base.file_dir.group_thumbnail_upload_path,
                    ),
                ),
                (
                    "background_color",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="group.Color",
                    ),
                ),
                (
                    "parent_group",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="group.GroupStructure",
                    ),
                ),
                (
                    "self_identify",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="group.GroupType",
                    ),
                ),
                (
                    "store",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="store_group_structure",
                        to="store.Store",
                    ),
                ),
            ],
            options={
                "verbose_name": "Group Structure",
                "verbose_name_plural": "Group Structures",
            },
        ),
        migrations.AddField(
            model_name="collection",
            name="group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="group.GroupStructure",
            ),
        ),
    ]

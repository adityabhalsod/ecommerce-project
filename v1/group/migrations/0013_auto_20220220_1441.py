# Generated by Django 3.0.8 on 2022-02-20 14:41

from django.db import migrations, models
import django.utils.timezone
import base.file_dir


class Migration(migrations.Migration):

    dependencies = [
        ("group", "0012_grouptype_display"),
    ]

    operations = [
        migrations.CreateModel(
            name="MultiplePhotos",
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
                    "original",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=base.file_dir.group_multiphotos_upload_path,
                    ),
                ),
                (
                    "webp_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=base.file_dir.group_multiphotos_webp_upload_path,
                    ),
                ),
                (
                    "thumbnail",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=base.file_dir.group_multiphotos_thumbnail_upload_path,
                    ),
                ),
                ("alt_text", models.TextField(default="")),
                ("is_default", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="groupstructure",
            name="multiple_photos",
            field=models.ManyToManyField(
                blank=True,
                related_name="group_multiple_photos",
                to="group.MultiplePhotos",
            ),
        ),
    ]

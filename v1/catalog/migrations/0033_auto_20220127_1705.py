# Generated by Django 3.0.8 on 2022-01-27 17:05

from django.db import migrations, models
import base.file_dir


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0032_auto_20220127_1653"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productphoto",
            name="thumbnail",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=base.file_dir.product_thumbnail_upload_path,
            ),
        ),
        migrations.AlterField(
            model_name="variationphoto",
            name="original",
            field=models.ImageField(
                blank=True, null=True, upload_to=base.file_dir.variation_upload_path
            ),
        ),
        migrations.AlterField(
            model_name="variationphoto",
            name="thumbnail",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=base.file_dir.variation_thumbnail_upload_path,
            ),
        ),
        migrations.AlterField(
            model_name="variationphoto",
            name="webp_image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=base.file_dir.variation_webp_upload_path,
            ),
        ),
    ]

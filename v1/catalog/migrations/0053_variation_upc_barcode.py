# Generated by Django 3.0.8 on 2022-02-20 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0052_auto_20220220_1402"),
    ]

    operations = [
        migrations.AddField(
            model_name="variation",
            name="upc_barcode",
            field=models.CharField(
                blank=True,
                default="",
                max_length=255,
                null=True,
                verbose_name="Universal Product Code",
            ),
        ),
    ]

# Generated by Django 3.0.8 on 2022-02-10 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0045_auto_20220205_1155"),
    ]

    operations = [
        migrations.AddField(
            model_name="productstockmaster",
            name="rack",
            field=models.CharField(blank=True, default="", max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="productstockmaster",
            name="row",
            field=models.CharField(blank=True, default="", max_length=255, null=True),
        ),
    ]

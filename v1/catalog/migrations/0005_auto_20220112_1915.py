# Generated by Django 3.0.8 on 2022-01-12 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_measurement"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name": "Category", "verbose_name_plural": "Categories"},
        ),
    ]

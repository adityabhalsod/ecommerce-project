# Generated by Django 3.0.8 on 2022-01-17 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0023_auto_20220117_1647"),
    ]

    operations = [
        migrations.RenameField(
            model_name="variation",
            old_name="product",
            new_name="product_stock_master",
        ),
    ]

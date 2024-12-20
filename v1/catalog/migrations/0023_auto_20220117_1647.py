# Generated by Django 3.0.8 on 2022-01-17 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0022_auto_20220117_1637"),
    ]

    operations = [
        migrations.AlterField(
            model_name="variation",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="stock_master_variation",
                to="catalog.ProductStockMaster",
            ),
        ),
    ]

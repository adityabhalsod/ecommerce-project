# Generated by Django 3.0.8 on 2022-02-05 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0044_auto_20220205_1143"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="unit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_unit",
                to="catalog.Unit",
            ),
        ),
    ]

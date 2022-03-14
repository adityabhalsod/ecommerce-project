# Generated by Django 3.0.8 on 2022-01-17 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0018_remove_productstockmaster_variation_quantity"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="unit",
        ),
        migrations.RemoveField(
            model_name="productstockmaster",
            name="variation",
        ),
        migrations.AddField(
            model_name="product",
            name="variation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="catalog.Variation",
            ),
        ),
    ]

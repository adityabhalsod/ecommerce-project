# Generated by Django 3.0.8 on 2022-01-17 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0020_auto_20220117_1629"),
    ]

    operations = [
        migrations.AddField(
            model_name="variation",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="catalog.Product",
            ),
        ),
    ]

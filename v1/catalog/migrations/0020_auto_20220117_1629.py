# Generated by Django 3.0.8 on 2022-01-17 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0019_auto_20220117_1627"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="variation",
        ),
        migrations.AddField(
            model_name="product",
            name="unit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="catalog.Unit",
            ),
        ),
    ]

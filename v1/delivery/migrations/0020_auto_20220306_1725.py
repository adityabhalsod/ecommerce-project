# Generated by Django 3.1.14 on 2022-03-06 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0009_auto_20220220_1814"),
        ("delivery", "0019_auto_20220305_1918"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="deliveryboy",
            name="store",
        ),
        migrations.AddField(
            model_name="deliveryboy",
            name="store",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="delivery_boy_store",
                to="store.store",
            ),
        ),
    ]

# Generated by Django 3.0.8 on 2022-02-05 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0022_finaldeliveredorder"),
    ]

    operations = [
        migrations.AddField(
            model_name="finaldeliveredorder",
            name="amount",
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]

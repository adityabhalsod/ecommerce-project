# Generated by Django 3.0.8 on 2022-02-14 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0011_auto_20220213_0523"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="referral_code",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="Referral code"
            ),
        ),
    ]

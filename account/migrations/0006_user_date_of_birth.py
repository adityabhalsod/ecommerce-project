# Generated by Django 3.0.8 on 2022-02-05 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0005_auto_20220127_1938"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True, verbose_name="date of birth"),
        ),
    ]

# Generated by Django 3.0.8 on 2022-02-23 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0013_auto_20220218_1724"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_online",
            field=models.BooleanField(default=False),
        ),
    ]

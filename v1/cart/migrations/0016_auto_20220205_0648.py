# Generated by Django 3.0.8 on 2022-02-05 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0015_auto_20220205_0644"),
    ]

    operations = [
        migrations.RenameField(
            model_name="checkout",
            old_name="is_membership_exist",
            new_name="new_membership_adding",
        ),
    ]

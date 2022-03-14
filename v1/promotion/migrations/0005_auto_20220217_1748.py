# Generated by Django 3.0.8 on 2022-02-17 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("promotion", "0004_discountvoucher_description"),
    ]

    operations = [
        migrations.RenameField(
            model_name="discountvoucher",
            old_name="is_exist_range_criteria",
            new_name="is_exist_min_amount",
        ),
        migrations.RenameField(
            model_name="discountvoucher",
            old_name="amount_ending_range",
            new_name="min_amount",
        ),
        migrations.RemoveField(
            model_name="discountvoucher",
            name="amount_starting_range",
        ),
    ]

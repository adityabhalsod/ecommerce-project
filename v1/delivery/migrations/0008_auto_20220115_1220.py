# Generated by Django 3.0.8 on 2022-01-15 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("delivery", "0007_auto_20220115_1214"),
    ]

    operations = [
        migrations.RenameField(
            model_name="deliveryboydocument",
            old_name="id_number",
            new_name="document_id_number",
        ),
        migrations.RenameField(
            model_name="deliveryboydocument",
            old_name="id_proof_type",
            new_name="document_type",
        ),
    ]

# Generated by Django 3.0.8 on 2022-01-15 12:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("delivery", "0005_auto_20220115_1130"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="DeliveryBoyIDProof",
            new_name="DeliveryBoyDocument",
        ),
        migrations.AddField(
            model_name="deliveryboypayoutinformation",
            name="payout_balance",
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name="deliveryboypayoutinformation",
            name="bank_account_ifsc_code",
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="deliveryboypayoutinformation",
            name="bank_account_number",
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]

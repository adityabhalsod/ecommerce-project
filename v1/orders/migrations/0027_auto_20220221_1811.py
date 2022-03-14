# Generated by Django 3.0.8 on 2022-02-21 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("promotion", "0008_auto_20220218_2238"),
        ("orders", "0026_order_transaction"),
    ]

    operations = [
        migrations.AddField(
            model_name="finaldeliveredorder",
            name="discount_and_voucher",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="individual_discount_and_voucher",
                to="promotion.DiscountVoucher",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="discount_and_voucher",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="order_discount_and_voucher",
                to="promotion.DiscountVoucher",
            ),
        ),
    ]

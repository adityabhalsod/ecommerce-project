# Generated by Django 3.1.14 on 2022-02-26 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("membership", "0004_auto_20220226_1924"),
    ]

    operations = [
        migrations.AddField(
            model_name="membershipplain",
            name="benefits",
            field=models.ManyToManyField(
                blank=True,
                related_name="plan_benefits",
                to="membership.MembershipBenefits",
            ),
        ),
    ]

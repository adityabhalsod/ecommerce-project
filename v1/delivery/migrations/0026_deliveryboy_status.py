# Generated by Django 3.1.14 on 2022-03-28 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0025_auto_20220328_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryboy',
            name='status',
            field=models.CharField(choices=[('approve', 'Approve'), ('reject', 'Reject'), ('pending', 'Pending')], default='pending', max_length=255),
        ),
    ]

# Generated by Django 3.1.14 on 2022-03-28 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0026_deliveryboy_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryboy',
            name='is_approve',
        ),
    ]
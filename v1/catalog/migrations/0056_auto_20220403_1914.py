# Generated by Django 3.1.14 on 2022-04-03 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0055_variation_open_stock'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='productphoto',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='productstockmaster',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='unit',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='variation',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='variationphoto',
            options={'ordering': ['-id']},
        ),
    ]

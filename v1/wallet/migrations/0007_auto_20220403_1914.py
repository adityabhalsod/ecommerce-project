# Generated by Django 3.1.14 on 2022-04-03 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0006_caseondeliverycollectionhistory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='caseondeliverycollectionhistory',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-id']},
        ),
    ]

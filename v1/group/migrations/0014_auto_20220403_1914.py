# Generated by Django 3.1.14 on 2022-04-03 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0013_auto_20220220_1441'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collection',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='color',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='grouptype',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='multiplephotos',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='productcollection',
            options={'ordering': ['-id']},
        ),
    ]

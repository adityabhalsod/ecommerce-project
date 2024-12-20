# Generated by Django 3.0.8 on 2022-01-23 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("group", "0005_productcollection_store"),
    ]

    operations = [
        migrations.AlterField(
            model_name="groupstructure",
            name="level",
            field=models.CharField(
                blank=True,
                choices=[("1", "Level 1"), ("2", "Level 2"), ("3", "Level 3")],
                default="1",
                max_length=5,
                null=True,
            ),
        ),
    ]

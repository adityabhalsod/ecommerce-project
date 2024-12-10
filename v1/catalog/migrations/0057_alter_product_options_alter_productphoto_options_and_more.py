# Generated by Django 5.1.3 on 2024-12-10 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0056_auto_20220403_1914"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={},
        ),
        migrations.AlterModelOptions(
            name="productphoto",
            options={},
        ),
        migrations.AlterModelOptions(
            name="productstockmaster",
            options={},
        ),
        migrations.AlterModelOptions(
            name="unit",
            options={},
        ),
        migrations.AlterModelOptions(
            name="variation",
            options={},
        ),
        migrations.AlterModelOptions(
            name="variationphoto",
            options={},
        ),
        migrations.AlterField(
            model_name="category",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="productphoto",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="productstockmaster",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="unit",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="variation",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="variationphoto",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]

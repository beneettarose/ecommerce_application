# Generated by Django 5.1.7 on 2025-03-30 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp_ecommerce", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                choices=[
                    ("common", "Common"),
                    ("women", "Women"),
                    ("accessories", "Accessories"),
                    ("new_arrival", "New Arrival"),
                ],
                max_length=50,
                unique=True,
            ),
        ),
    ]

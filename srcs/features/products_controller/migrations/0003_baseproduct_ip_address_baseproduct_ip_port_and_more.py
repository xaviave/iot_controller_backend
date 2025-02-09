# Generated by Django 4.2.12 on 2024-06-10 14:18

import colorfield.fields
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products_controller", "0002_alter_patternmode_palette"),
    ]

    operations = [
        migrations.AddField(
            model_name="baseproduct",
            name="ip_address",
            field=models.GenericIPAddressField(default="0.0.0.0"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="baseproduct",
            name="ip_port",
            field=models.IntegerField(
                default=50051,
                validators=[
                    django.core.validators.MaxValueValidator(65536),
                    django.core.validators.MinValueValidator(0),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="patternmode",
            name="palette",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=colorfield.fields.ColorField(default="#FFFF", image_field=None, max_length=25, samples=None),
                size=None,
            ),
        ),
    ]

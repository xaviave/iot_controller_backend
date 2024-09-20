# Generated by Django 4.2.11 on 2024-03-27 09:23

import colorfield.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import features.products_controller.models.products.coffee_machine


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BaseProduct",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, unique=True)),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, unique=True)),
            ],
            options={
                "verbose_name_plural": "categories",
            },
        ),
        migrations.CreateModel(
            name="LedMode",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, unique=True)),
                (
                    "polymorphic_ctype",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="polymorphic_%(app_label)s.%(class)s_set+",
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
        ),
        migrations.CreateModel(
            name="CoffeeMachine",
            fields=[
                (
                    "baseproduct_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="products_controller.baseproduct",
                    ),
                ),
                ("status", models.IntegerField(choices=[(1, "ON"), (2, "OFF"), (3, "ERROR")])),
                ("heat", models.FloatField(default=0.0)),
                (
                    "water_level",
                    models.IntegerField(
                        choices=[(0, "EMPTY"), (1, "WARNING"), (2, "FULL")],
                        default=features.products_controller.models.products.coffee_machine.ContainerStatus["EMPTY"],
                    ),
                ),
                (
                    "used_water_level",
                    models.IntegerField(
                        choices=[(0, "EMPTY"), (1, "WARNING"), (2, "FULL")],
                        default=features.products_controller.models.products.coffee_machine.ContainerStatus["EMPTY"],
                    ),
                ),
                (
                    "coffee_level",
                    models.IntegerField(
                        choices=[(0, "EMPTY"), (1, "WARNING"), (2, "FULL")],
                        default=features.products_controller.models.products.coffee_machine.ContainerStatus["EMPTY"],
                    ),
                ),
                ("filter_position", models.BooleanField(default=True)),
                ("mode_value", models.IntegerField(default=0)),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            bases=("products_controller.baseproduct",),
        ),
        migrations.CreateModel(
            name="ColorMode",
            fields=[
                (
                    "ledmode_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="products_controller.ledmode",
                    ),
                ),
                (
                    "color",
                    colorfield.fields.ColorField(default="#FFFFFF", image_field=None, max_length=25, samples=None),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            bases=("products_controller.ledmode",),
        ),
        migrations.CreateModel(
            name="ImageMode",
            fields=[
                (
                    "ledmode_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="products_controller.ledmode",
                    ),
                ),
                ("image", models.ImageField(upload_to="images/")),
                ("image_low_pixel", models.ImageField(blank=True, null=True, upload_to="low_pixel_images/")),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            bases=("products_controller.ledmode",),
        ),
        migrations.CreateModel(
            name="PatternMode",
            fields=[
                (
                    "ledmode_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="products_controller.ledmode",
                    ),
                ),
                ("fps", models.DecimalField(decimal_places=2, max_digits=5)),
                ("blink", models.DecimalField(decimal_places=2, max_digits=4)),
                (
                    "palette",
                    models.CharField(
                        choices=[
                            ("Cloud", "Cloud"),
                            ("Heat", "Heat"),
                            ("Lava", "Lava"),
                            ("Ocean", "Ocean"),
                            ("Party", "Party"),
                            ("Rainbow", "Rainbow"),
                        ]
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            bases=("products_controller.ledmode",),
        ),
        migrations.CreateModel(
            name="VideoMode",
            fields=[
                (
                    "ledmode_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="products_controller.ledmode",
                    ),
                ),
                ("video", models.FileField(upload_to="videos/")),
                ("video_low_pixel", models.ImageField(blank=True, null=True, upload_to="video_low_pixels/")),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            bases=("products_controller.ledmode",),
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("pub_date", models.DateTimeField(verbose_name="date published")),
                ("name", models.CharField(max_length=200, unique=True)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ("products", models.ManyToManyField(to="products_controller.baseproduct")),
            ],
        ),
        migrations.AddField(
            model_name="baseproduct",
            name="categories",
            field=models.ManyToManyField(to="products_controller.category"),
        ),
        migrations.AddField(
            model_name="baseproduct",
            name="polymorphic_ctype",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="polymorphic_%(app_label)s.%(class)s_set+",
                to="contenttypes.contenttype",
            ),
        ),
        migrations.CreateModel(
            name="LedPanel",
            fields=[
                (
                    "baseproduct_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="products_controller.baseproduct",
                    ),
                ),
                ("status", models.IntegerField(choices=[(1, "ON"), (2, "OFF"), (3, "ERROR")])),
                ("brightness", models.DecimalField(decimal_places=2, default=0.5, max_digits=3)),
                (
                    "mode",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to="products_controller.ledmode"
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            bases=("products_controller.baseproduct",),
        ),
    ]

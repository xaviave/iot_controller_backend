# Generated by Django 4.2.9 on 2024-01-23 13:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products_controller", "0009_alter_coffeemachine_coffee_level_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="patternmode",
            name="status",
        ),
        migrations.AddField(
            model_name="patternmode",
            name="blink",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="patternmode",
            name="fps",
            field=models.DecimalField(decimal_places=2, default=30, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="patternmode",
            name="palette",
            field=models.CharField(
                choices=[
                    ("Cloud", "Cloud"),
                    ("Heat", "Heat"),
                    ("Lava", "Lava"),
                    ("Ocean", "Ocean"),
                    ("Party", "Party"),
                    ("Rainbow", "Rainbow"),
                ],
                default=1,
            ),
            preserve_default=False,
        ),
    ]

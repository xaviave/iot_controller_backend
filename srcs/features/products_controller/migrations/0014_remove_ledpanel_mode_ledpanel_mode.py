# Generated by Django 4.2.10 on 2024-03-04 14:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products_controller", "0013_remove_ledpanel_mode_ledpanel_mode"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ledpanel",
            name="mode",
        ),
        migrations.AddField(
            model_name="ledpanel",
            name="mode",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="products_controller.ledmode"
            ),
        ),
    ]

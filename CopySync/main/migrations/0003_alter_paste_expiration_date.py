# Generated by Django 4.2.10 on 2024-05-05 03:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_paste_type_paste_user_alter_paste_expiration_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paste",
            name="expiration_date",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(
                    2024, 5, 6, 3, 55, 46, 168493, tzinfo=datetime.timezone.utc
                ),
                null=True,
            ),
        ),
    ]

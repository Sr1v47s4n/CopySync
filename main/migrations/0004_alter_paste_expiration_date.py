# Generated by Django 4.2.10 on 2024-05-05 03:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0003_alter_paste_expiration_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paste",
            name="expiration_date",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(
                    2024, 5, 6, 3, 56, 13, 323979, tzinfo=datetime.timezone.utc
                ),
                null=True,
            ),
        ),
    ]

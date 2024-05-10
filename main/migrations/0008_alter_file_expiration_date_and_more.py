# Generated by Django 4.2.10 on 2024-05-10 03:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0007_alter_file_content_alter_file_expiration_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="file",
            name="expiration_date",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(
                    2024, 5, 10, 9, 52, 47, 756832, tzinfo=datetime.timezone.utc
                ),
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="paste",
            name="expiration_date",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(
                    2024, 5, 11, 3, 52, 47, 650707, tzinfo=datetime.timezone.utc
                ),
                null=True,
            ),
        ),
    ]
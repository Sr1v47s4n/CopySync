# Generated by Django 4.2.10 on 2024-05-05 03:38

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Paste",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "expiration_date",
                    models.DateTimeField(
                        blank=True,
                        default=datetime.datetime(
                            2024, 5, 6, 3, 38, 52, 706123, tzinfo=datetime.timezone.utc
                        ),
                        null=True,
                    ),
                ),
                ("url", models.CharField(max_length=10, unique=True)),
            ],
        ),
    ]
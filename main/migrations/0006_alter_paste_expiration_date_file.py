# Generated by Django 4.2.10 on 2024-05-10 02:30

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0005_alter_paste_expiration_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paste",
            name="expiration_date",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(
                    2024, 5, 11, 2, 30, 45, 315786, tzinfo=datetime.timezone.utc
                ),
                null=True,
            ),
        ),
        migrations.CreateModel(
            name="File",
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
                ("content", models.FileField(upload_to="shared/")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "expiration_date",
                    models.DateTimeField(
                        blank=True,
                        default=datetime.datetime(
                            2024, 5, 11, 2, 30, 45, 406520, tzinfo=datetime.timezone.utc
                        ),
                        null=True,
                    ),
                ),
                ("url", models.CharField(max_length=10, unique=True)),
                ("type", models.CharField(default="public", max_length=10)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

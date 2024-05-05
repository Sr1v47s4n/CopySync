from django.db import models
from django.utils import timezone


class Paste(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateTimeField(
        null=True, blank=True, default=(timezone.now() + timezone.timedelta(days=1))
    )
    url = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=10, default="public")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, blank=True)
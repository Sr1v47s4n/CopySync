from django.db import models
from django.utils import timezone
from django.core.validators import MaxLengthValidator
import os
class Paste(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateTimeField(
        null=True, blank=True, default=(timezone.now() + timezone.timedelta(days=1))
    )
    url = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=10, default="public")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, blank=True)


class File(models.Model):
    content = models.FileField(
        upload_to="shared/",
        validators=[
            MaxLengthValidator(20 * 1024 * 1024
            )  # Limit file size to 20MB
        ]
    )
    created_at = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateTimeField(
        null=True, blank=True, default=(timezone.now() + timezone.timedelta(hours=6))
    )
    url = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=10, default="public")
    user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, null=True, blank=True
    )
    
    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem
        if self.content:
            os.remove(self.content.path)
        # Call the parent class' delete method
        super().delete(*args, **kwargs)

from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    location = models.CharField(max_length=30, blank=True)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile of {self.user.username}"

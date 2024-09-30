from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="profile_picture/")

    def __str__(self) -> str:
        return f"{self.user.name}"

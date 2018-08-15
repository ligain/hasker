from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    avatar = models.ImageField()
    created_at = models.DateTimeField(default=timezone.now)


def get_stub_user():
    return User.objects.get_or_create(
        username="anonymous",
        email="anonymous@example.com"
    )[0]

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from hasker.profiles.models import get_stub_user


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    tags = models.ManyToManyField("Tag", blank=True, related_name="questions")
    author = models.ForeignKey(User, on_delete=models.SET(get_stub_user), related_name="questions")
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, null=True)


class Answer(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET(get_stub_user), related_name="answers")
    created_at = models.DateTimeField(default=timezone.now)
    is_right = models.BooleanField(default=False)


class Tag(models.Model):
    name = models.CharField(max_length=100)

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum

from hasker.profiles.models import get_stub_user


VOTE_CHOISES = (
    (-1, 'down'),
    (0, 'none'),
    (1, 'up')
)


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    tags = models.ManyToManyField("Tag", blank=True, related_name="questions")
    author = models.ForeignKey(User, on_delete=models.SET(get_stub_user), related_name="questions")
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, null=True)
    votes = GenericRelation("Vote")

    @property
    def rating(self):
        rating_dict = self.votes.aggregate(Sum('value'))
        if rating_dict.get('value__sum') is None:
            return 0
        return rating_dict.get('value__sum')


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET(get_stub_user), related_name="answers")
    created_at = models.DateTimeField(default=timezone.now)
    is_right = models.BooleanField(default=False)
    votes = GenericRelation("Vote")

    @property
    def rating(self):
        rating_dict = self.votes.aggregate(Sum('value'))
        if rating_dict.get('value__sum') is None:
            return 0
        return rating_dict.get('value__sum')


class Tag(models.Model):
    name = models.CharField(max_length=100)


class Vote(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET(get_stub_user), related_name="votes")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    receiver = GenericForeignKey('content_type', 'object_id')
    value = models.SmallIntegerField(choices=VOTE_CHOISES, default=0)


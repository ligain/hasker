from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Sum

from hasker.profiles.models import get_stub_user


VOTE_CHOISES = (
    (-1, 'down'),
    (0, 'none'),
    (1, 'up')
)


class VoteReceiver(models.Model):
    @property
    def votes(self):
        return self.votereceiver_ptr.vote_set.all()

    @property
    def rating(self):
        rating_dict = self.votes.aggregate(Sum('value'))
        if rating_dict.get('value__sum') is None:
            return 0
        return rating_dict.get('value__sum')


class Question(VoteReceiver):
    title = models.CharField(max_length=255)
    text = models.TextField()
    tags = models.ManyToManyField("Tag", blank=True, related_name="questions")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET(get_stub_user), related_name="questions")
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, null=True)
    right_answer = models.ForeignKey("Answer", on_delete=models.SET_NULL,
                                     related_name="right_for_question", null=True, blank=True)


class Answer(VoteReceiver):
    parent_question = models.ForeignKey(Question, on_delete=models.SET_NULL,
                                        related_name="answers", null=True, blank=True)
    text = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.SET(get_stub_user), related_name="answers")
    created_at = models.DateTimeField(default=timezone.now)


class Tag(models.Model):
    name = models.CharField(max_length=100)


class Vote(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.SET(get_stub_user), related_name="votes")
    receiver = models.ForeignKey(VoteReceiver, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    value = models.SmallIntegerField(choices=VOTE_CHOISES, default=0)


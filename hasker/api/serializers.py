from django.contrib.auth.models import User
from rest_framework import serializers

from hasker.core.models import Vote


class VoteSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Vote
        fields = ('author', 'content_type', 'object_id', 'value')

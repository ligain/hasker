from rest_framework import serializers

from hasker.core.models import Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('value', 'object_id', 'content_type')

    def update(self, instance, validated_data):
        return instance

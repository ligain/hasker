from django.contrib.auth.models import User
from rest_framework import serializers

from hasker.core.models import Vote, Answer


class AuthorValidator:

    message = 'Only author of question can choose right answer.'

    def set_context(self, serializer_field):
        self.question = getattr(serializer_field.instance, 'question', None)
        self.user = serializer_field.context['request'].user

    def __call__(self, *args, **kwargs):
        if self.question.author != self.user:
            raise serializers.ValidationError(self.message)


class VoteSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Vote
        fields = ('author', 'content_type', 'object_id', 'value')


class AnswerSerializer(serializers.ModelSerializer):

    def validate_is_right(self, value):
        message = 'The right answer is already selected'
        question = self.instance.question
        right_answer = question.answers.filter(is_right=True).first()
        if not right_answer:
            return value
        elif right_answer.id != self.instance.id:
            # Trying to mark another answer as right
            raise serializers.ValidationError(message)
        return value

    class Meta:
        model = Answer
        fields = ('is_right', )
        validators = [
            AuthorValidator(),
        ]

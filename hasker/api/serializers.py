from django.contrib.auth import get_user_model

from rest_framework import serializers

from hasker.core.models import Vote, VoteReceiver, Question


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
        queryset=get_user_model().objects.all(),
        default=serializers.CurrentUserDefault()
    )
    receiver = serializers.PrimaryKeyRelatedField(
        queryset=VoteReceiver.objects.all()
    )

    class Meta:
        model = Vote
        fields = ('author', 'receiver', 'value')


class RightAnswerSerializer(serializers.ModelSerializer):

    def validate_right_answer(self, value):
        message = 'The right answer is already selected'
        right_answer = self.instance.question.right_answer
        if right_answer and right_answer != value:
            raise serializers.ValidationError(message)
        return value

    class Meta:
        model = Question
        fields = ('right_answer', )
        validators = [
            AuthorValidator(),
        ]

    def save(self, **kwargs):
        if self.instance.right_answer == self.validated_data['right_answer']:
            self.validated_data['right_answer'] = None
        return super().save(**kwargs)

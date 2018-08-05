from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from hasker.core.models import Vote, Answer


class UniqueAnswer():
    pass

# class UniqueValidator(object):
#     """
#     Validator that corresponds to `unique=True` on a model field.
#
#     Should be applied to an individual field on the serializer.
#     """
#     message = _('This field must be unique.')
#
#     def __init__(self, queryset, message=None, lookup='exact'):
#         self.queryset = queryset
#         self.serializer_field = None
#         self.message = message or self.message
#         self.lookup = lookup
#
#     def set_context(self, serializer_field):
#         """
#         This hook is called by the serializer instance,
#         prior to the validation call being made.
#         """
#         # Determine the underlying model field name. This may not be the
#         # same as the serializer field name if `source=<>` is set.
#         self.field_name = serializer_field.source_attrs[-1]
#         # Determine the existing instance, if this is an update operation.
#         self.instance = getattr(serializer_field.parent, 'instance', None)
#
#     def filter_queryset(self, value, queryset):
#         """
#         Filter the queryset to all instances matching the given attribute.
#         """
#         filter_kwargs = {'%s__%s' % (self.field_name, self.lookup): value}
#         return qs_filter(queryset, **filter_kwargs)
#
#     def exclude_current_instance(self, queryset):
#         """
#         If an instance is being updated, then do not include
#         that instance itself as a uniqueness conflict.
#         """
#         if self.instance is not None:
#             return queryset.exclude(pk=self.instance.pk)
#         return queryset
#
#     def __call__(self, value):
#         queryset = self.queryset
#         queryset = self.filter_queryset(value, queryset)
#         queryset = self.exclude_current_instance(queryset)
#         if qs_exists(queryset):
#             raise ValidationError(self.message, code='unique')


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
        print(1)

    class Meta:
        model = Answer
        fields = ('is_right', )
        # validators = [
        #     UniqueAnswer(),
        #     UniqueValidator
        # ]

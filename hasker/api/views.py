import re

from django.db.models import Sum, Value, Q
from django.db.models.functions import Coalesce
from rest_framework import status
from rest_framework.generics import GenericAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from hasker.api.serializers import VoteSerializer, RightAnswerSerializer, QuestionSerializer, TrendingSerializer, \
    AnswerSerializer
from hasker.core.context_processors import trending
from hasker.core.forms import QueryForm
from hasker.core.models import Vote, Question, Answer


class VoteApiView(GenericAPIView):
    serializer_class = VoteSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            vote, _ = Vote.objects.get_or_create(
                author=serializer.validated_data.get('author'),
                receiver=serializer.validated_data.get('receiver'),
            )
            vote.value = serializer.validated_data.get('value', 0)
            vote.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RightAnswerUpdateApiView(UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = RightAnswerSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class MainPageApiView(ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.all().order_by('-created_at')
        ordering = self.request.query_params.get('order_by')
        if ordering == 'hot':
            queryset = queryset.annotate(
                votes_rating=Coalesce(Sum('votereceiver_ptr__vote__value'), Value(0))
            ).order_by('-votes_rating')
        return queryset


class TrendingApiView(ListAPIView):
    serializer_class = TrendingSerializer

    def get_queryset(self):
        return trending(self.request).get('trending_questions', Question.objects.none())


class QuestionApiView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'slug'


class QuestionAnswersApiView(ListAPIView):
    serializer_class = AnswerSerializer

    def get_queryset(self):
        question_slug = self.kwargs.get('slug')
        queryset = Answer.objects.filter(parent_question__slug=question_slug)
        return queryset


class StringSearchApiView(ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        query_form = QueryForm(self.kwargs)
        if query_form.is_valid():
            queryset = Question.objects.filter(
                Q(title__icontains=query_form.cleaned_data['q']) |
                Q(text__icontains=query_form.cleaned_data['q'])
            ).annotate(
                votes_rating=Coalesce(Sum('votereceiver_ptr__vote__value'), Value(0))
            ).order_by('-votes_rating', '-created_at')
        else:
            queryset = Question.objects.none()
        return queryset


class TagSearchApiView(ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        tag_name = self.kwargs.get('tag')
        if tag_name:
            queryset = Question.objects.filter(tags__name=tag_name)
        else:
            queryset = Question.objects.none()
        return queryset
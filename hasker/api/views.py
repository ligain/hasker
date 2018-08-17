from rest_framework import status
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.response import Response

from hasker.api.serializers import VoteSerializer, RightAnswerSerializer
from hasker.core.models import Vote, Answer, Question


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
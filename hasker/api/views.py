from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from hasker.api.serializers import VoteSerializer
from hasker.core.models import Vote


class VoteApiView(GenericAPIView):
    serializer_class = VoteSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            vote, _ = Vote.objects.get_or_create(
                author=serializer.validated_data.get('author'),
                content_type=serializer.validated_data.get('content_type'),
                object_id=serializer.validated_data.get('object_id'),
            )
            vote.value = serializer.validated_data.get('value', 0)
            vote.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

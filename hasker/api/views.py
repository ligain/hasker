from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from hasker.api.serializers import VoteSerializer
from hasker.core.models import Vote


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Vote.objects.all()
        serializer = VoteSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
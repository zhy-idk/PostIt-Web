from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import PostModel
from .serializer import PostSerializer

# Create your views here.
@api_view(['GET'])
def get_posts(request):
    airlines = PostModel.objects.all()
    serializedData = PostSerializer(airlines, many=True).data
    return Response(serializedData)
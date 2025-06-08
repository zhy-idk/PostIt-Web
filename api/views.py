from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import PostModel
from .serializer import PostSerializer

# Create your views here.
@api_view(['GET'])
def get_posts(request):
    posts = PostModel.objects.all().order_by('-created_at')
    serializedData = PostSerializer(posts, many=True).data
    return Response(serializedData)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_post_api(request, user_id):
    posts = PostModel.objects.filter(user_id=user_id).order_by('-created_at')
    serializedData = PostSerializer(posts, many=True).data
    return Response(serializedData)

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
        })
    return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_post_api(request):
    # Create a mutable copy and attach user ID
    data = request.data.copy()
    data['user'] = request.user.id  # manually set the user ID

    serializer = PostSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # ensure the user is set as the authenticated user
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

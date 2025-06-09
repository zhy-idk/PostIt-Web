from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import PostModel
from .serializer import PostSerializer

from django.core.exceptions import ValidationError

# Create your views here.
@api_view(['GET'])
def get_posts(request):
    posts = PostModel.objects.all().order_by('-created_at')
    serializedData = PostSerializer(posts, many=True).data
    return Response(serializedData)

@api_view(['GET'])
def post_detail_api(request, post_id):
    try:
        post = PostModel.objects.get(id=post_id)
    except PostModel.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    serializedData = PostSerializer(post).data
    return Response(serializedData, status=status.HTTP_200_OK)

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
def register_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    password2 = request.data.get('password2')

    if not username or not password or not password2:
        return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if password != password2:
        return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        validate_password(password)
    except ValidationError as e:
        return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_api(request):
    # Delete the token to force login again
    request.user.auth_token.delete()
    return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_post_api(request):
    
    data = request.data.copy()
    data['user'] = request.user.id  # manually set the user ID

    serializer = PostSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # ensure the user is set as the authenticated user
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_post_api(request, post_id):
    try:
        post = PostModel.objects.get(id=post_id)
    except PostModel.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    # Ensure only the owner can edit
    if post.user != request.user:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    data = request.data.copy()
    if 'banner' in request.FILES:
        data['banner'] = request.FILES['banner']

    serializer = PostSerializer(post, data=data, partial=True) 
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post_api(request, post_id):
    try:
        post = PostModel.objects.get(id=post_id)
    except PostModel.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    # Only allow the post owner to delete
    if post.user != request.user:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    post.delete()
    return Response({'message': 'Post deleted successfully'}, status=status.HTTP_200_OK)
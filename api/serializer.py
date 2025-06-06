from rest_framework import serializers
from .models import PostModel

class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    created_at = serializers.DateTimeField(format="%B %d, %Y, %I:%M %p")
    class Meta:
        model = PostModel
        fields = '__all__' 
        read_only_fields = ('id',)
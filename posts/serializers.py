from rest_framework import serializers
from .models import Post
from comment_reply.serializers import *

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ("id", "content", "created_at", "post_images", "category", "comments")


class PostsLikesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ['id', 'user',]

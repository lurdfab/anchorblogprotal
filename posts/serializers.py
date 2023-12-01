from rest_framework import serializers
from .models import Post
from comment_reply.serializers import *


class PostReplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ("id", "user", "parent", "reply", "content", "created_at")


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ("id", "content", "created_at", "post_images", "category", "comments")

    def get_comments(self, obj):
        return PostReplySerializer(obj.get_thread(), many=True).data

class PostsLikesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ['id', 'user',]

class PostCommentsSerialiser(serializers.Serializer):
    comment = serializers.CharField(required=True)


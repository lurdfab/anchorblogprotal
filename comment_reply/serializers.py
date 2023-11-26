from rest_framework import serializers
from .models import *


class ReplySerializer(serializers.ModelSerializer):
    replied_by = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Reply
        fields = ( "comment", "reply", "reply_image", "replied_by")

    
class ReplyLikesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Reply
        fields = ['id', 'user',]


class CommentSerializer(serializers.ModelSerializer):
    commented_by = serializers.ReadOnlyField(source="user.username")
    replies = ReplySerializer(many=True, read_only=True)
    

    class Meta:
        model = Comment
        fields = ("post", "comment", "commented_at", "comment_image", "commented_by", "replies")

class CommentLikesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ['id', 'user',]
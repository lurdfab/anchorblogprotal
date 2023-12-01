from rest_framework import serializers
from .models import Video, Music
from comment_reply.serializers import *

class VideoSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Video
        fields = ("id", "title", "category", "description", "file", "comments")

class VideoLikesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Video
        fields = ['id', 'user',]

class MusicSerializer(serializers.ModelSerializer):
    comments = MusicCommentSerializer(many=True, read_only=True)
    class Meta:
        model = Music
        fields = ("id", "title", "category", "description", "file", "comments")


class MusicLikesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Music
        fields = ['id', 'user',]
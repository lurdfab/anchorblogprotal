from rest_framework import serializers
from .models import Post, PostComment
from user.serializers import UserSerializer
from likes import services


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ("id", "content", "post_type", "created_at", "updated_at", "post_media", "category", "likes", "comments" )

    def get_comments(self, obj):
        comment =  PostComment.objects.filter(post=obj, is_removed=False, parent=None)
        return PostCommentSerializer(comment, many=True).data

    def get_likes(self, obj):
        likes = services.get_fans(obj)
        return UserSerializer(likes, many=True).data

class PostsLikesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ['id', 'user',]

class PostCommentSerializer(serializers.ModelSerializer):
    # comment = serializers.ReadOnlyField(source='_get_comment')
    edited = serializers.ReadOnlyField(source='is_edited')
    child_count = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = (
            'id', 'user',  '_comment',
            'created_at', 'edited', 'is_removed', 'likes',
            'updated_at', 'is_nesting_permitted', 'child_count', 'parent', 'post'
        )
        read_only_fields = (
            'id', 'created_at', 'updated_at', 'child_count')

    def get_child_count(self, obj):
        replies = PostComment.objects\
            .filter(parent=obj)\
            .exclude(is_removed=True)
        return PostCommentSerializer(replies, many=True).data
    
    def get_likes(self, obj):
        likes = services.get_fans(obj)
        return UserSerializer(likes, many=True).data

class PostCommentCreateSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(max_length=3000, min_length=4)
    edited = serializers.ReadOnlyField(source='is_edited')
    child_count = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = (
            'id', 'user', 'comment','post',
            'parent', 'is_nesting_permitted', 'child_count', 'edited'
        )
        read_only_fields = ('child_count')
        extra_kwargs = {
            'post': {'write_only': True}
        }

    def create(self, validated_data):
        comment = validated_data.pop('comment')
        validated_data['_comment'] = comment
        comment = PostComment.objects.create(**validated_data)
        return comment

    def update(self, instance, validated_data):
        comment = validated_data.pop('comment')
        validated_data['_comment'] = comment
        instance._comment = comment
        instance.save()
        return instance

    def get_child_count(self, obj):
        return 0
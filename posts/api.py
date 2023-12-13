from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import viewsets, permissions, status
from user.permissions import *
from likes.mixins import *
from django.db import models
from django.db.models import Q, F
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from posts.models import Post
from .serializers import PostCommentCreateSerializer
import copy
from django.shortcuts import get_object_or_404 



class PostViewset(LikedResourceMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_class = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self): #this is for one model

        if self.action == "like":
            self.permission_class = (permissions.IsAuthenticated,)

        if self.action == "unlike":
            self.permission_class = (permissions.IsAuthenticated,)

        return super().get_permissions()
    
    
    
    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)




class PostCommentPagination(PageNumberPagination):
    page_size = 24


class PostCommentViewSet(LikedResourceMixin, viewsets.ModelViewSet):
    queryset = PostComment.objects.all()
    pagination_class = PostCommentPagination
    serializer_class = PostCommentSerializer
    serializer_action_classes = {
        'list' : PostCommentSerializer,
        'create' : PostCommentCreateSerializer,
        'update' : PostCommentCreateSerializer,
    }

    def get_queryset(self):
        queryset = self.queryset.filter(is_removed=True)
        if self.kwargs != {}:
            if 'post_id' in self.kwargs:
                return self.queryset.filter(post__id=self.kwargs['post_id'])
        return queryset

    def list(self, request, post_id=None):
        deleted_with_children = PostComment.objects\
            .filter(
                parent=None,
                post__id=post_id,
                is_removed=True)\
            .exclude(comments=None).distinct()
        queryset = self.get_queryset().filter(parent=None, is_removed=False).distinct()
        queryset = queryset | deleted_with_children
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, post_id=None):
        data = copy.deepcopy(request.data)
        # data = request.data
      

        if not request.user.is_authenticated:
            return Response(
                {'error': 'User not authorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if int(data['user']) != request.user.pk:
            
            return Response(
                {'error': 'spoofing detected'},
                status=status.HTTP_403_FORBIDDEN
            )
        if post_id is not None:
            try:
                data['post'] = Post.objects.get(id=post_id).pk
            except Post.DoesNotExist:
                return Response({'error': 'Wrong id'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Error in route'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data)
        if serializer.is_valid():
            comment = serializer.save()
          
            serializer = PostCommentSerializer(instance=comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, post_id=None, pk=None):
        data = request.data
        comment = self.get_object()

        if not request.user.is_authenticated:
            return Response({'error': 'The user is anonymous'}, status=status.HTTP_401_UNAUTHORIZED)
        if data['user'] != request.user.pk:
            return Response({'error': 'spoofing detected'}, status=status.HTTP_403_FORBIDDEN)

        if post_id is not None:
            try:
                data['post'] = Post.objects.get(id=post_id).pk
            except Post.DoesNotExist:
                return Response({'error': 'Wrong id'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Error in route'}, status=status.HTTP_400_BAD_REQUEST)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data,instance=comment)
        if serializer.is_valid():
            comment = serializer.save()
            serializer = PostCommentSerializer(instance=comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, post_id=None, pk=None):
        comment = self.get_object()
        user = request.user
        if comment.user != user:
            return Response (
                {'error' : 'User not authorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        comment.is_removed = True
        comment.save()
        return Response({'success': True}, status=status.HTTP_200_OK)

    @action(detail=True)
    def children(self, request, post_id=None, pk=None):
        comment = self.get_object()
        children_comments = PostComment.objects.filter(parent=comment)
        deleted_with_children = children_comments.filter(is_removed=True)\
            .exclude(comments=None).distinct()
        queryset = children_comments.filter(is_removed=False).distinct()
        queryset = queryset | deleted_with_children
        return self.paginated_response(queryset)


  




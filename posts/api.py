from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import viewsets, permissions, status
from user.permissions import *
from likes.mixins import *


class PostViewset(LikedResourceMixin, viewsets.ModelViewSet):
    queryset = Post.objects.filter(reply=False)
    serializer_class = PostSerializer
    permission_class = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):

        if self.action == "like":
            self.permission_class = (permissions.IsAuthenticated,)

        if self.action == "unlike":
            self.permission_class = (permissions.IsAuthenticated,)

        return super().get_permissions()
    
    @action(detail=True, methods=["POST"])
    def postcomments(self, request, *args, **kwargs):
        parent = self.get_object()
        serializer = PostCommentsSerialiser(data=request.data, many=False)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        post = parent.reply_this(request.user, serializer.data.get("comment"))
        data = PostReplySerializer(post).data
        return Response(data, status=status.HTTP_200_OK)
    
    def get_serializer(self, *args, **kwargs):
        
        if self.action == "postcomments":
            self.serializer_class = PostCommentsSerialiser
        
        return super().get_serializer(*args, **kwargs)
    



class PostReplyViewset(LikedResourceMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_class = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):

        if self.action == "like":
            self.permission_class = (permissions.IsAuthenticated,)

        if self.action == "unlike":
            self.permission_class = (permissions.IsAuthenticated,)

        return super().get_permissions()
    
    @action(detail=True, methods=["POST"])
    def postreplies(self, request, *args, **kwargs):
        parent = Post.objects.get(id=self.kwargs["pk"])
        serializer = PostCommentsSerialiser(data=request.data, many=False)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        post = parent.reply_this(request.user, serializer.data.get("comment"))
        data = PostReplySerializer(post).data
        return Response(data, status=status.HTTP_200_OK)
    
    def get_serializer(self, *args, **kwargs):
        
        if self.action == "postreplies":
            self.serializer_class = PostCommentsSerialiser
        
        return super().get_serializer(*args, **kwargs)
    
    def get_queryset(self):
        qs = super().get_queryset()
        if self.kwargs.get("pk"):
            qs.filter(id=self.kwargs["pk"])
        else:
            qs.filter(parent=self.kwargs["id"])
        return qs
        
        






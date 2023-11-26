from .serializers import *
from .models import *
from rest_framework import viewsets, permissions, status
from user.permissions import *
from likes.mixins import *


class CommentViewset(LikedResourceMixin,viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):

        if self.action == "like":
            self.permission_class = (permissions.IsAuthenticated,)

        if self.action == "unlike":
            self.permission_class = (permissions.IsAuthenticated,)

        return super().get_permissions()

class ReplyViewSet(LikedResourceMixin,viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):

        if self.action == "like":
            self.permission_class = (permissions.IsAuthenticated,)

        if self.action == "unlike":
            self.permission_class = (permissions.IsAuthenticated,)

        return super().get_permissions()


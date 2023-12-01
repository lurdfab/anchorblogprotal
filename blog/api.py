from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import viewsets, permissions, status
from user.permissions import *
from likes.mixins import *


class VideoViewset(LikedResourceMixin, viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_class = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):

        if self.action == "like":
            self.permission_class = (permissions.IsAuthenticated,)

        if self.action == "unlike":
            self.permission_class = (permissions.IsAuthenticated,)

        return super().get_permissions()


class MusicViewset(LikedResourceMixin, viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    permission_class = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):

        if self.action == "like":
            self.permission_class = (permissions.IsAuthenticated,)

        if self.action == "unlike":
            self.permission_class = (permissions.IsAuthenticated,)

        return super().get_permissions()





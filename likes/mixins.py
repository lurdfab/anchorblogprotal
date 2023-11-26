from rest_framework.decorators import action
from rest_framework.response import Response
from . import services


class LikedResourceMixin:

    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        obj = self.get_object()
        services.add_like(obj, user=request.user)
        return Response()
    
    @action(detail=True, methods=['POST'])
    def unlike(self, request, pk=None):
        obj = self.get_object()
        services.remove_like(obj, user=request.user)
        return Response()
from rest_framework import generics
from blog.apps.blog.models import Post
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response

from blog.apps.blog.models import Post
from django.shortcuts import get_object_or_404

from .serializers import PostSerializer


class PostUserWritePermission(BasePermission):  # custom permisson
    message = "Editing posts is restricted to the author only"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:  # SAFE_METHODS is a tuple containing 'GET', 'OPTIONS' and 'HEAD'
            return True

        return obj.author == request.user


class PostList(viewsets.ModelViewSet):
    permission_classes = [PostUserWritePermission]
    serializer_class = PostSerializer
    # queryset = Post.objects.all() --> standard queryset

    def get_object(self, queyset=None, **kwargs):
        item = self.kwargs.get("pk")

        return get_object_or_404(Post, slug=item)

    def get_queryset(self):  # Custom queryset
        return Post.objects.all()


"""       
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
VIEWSETS APPROACH


class PostList(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def list(self, request):
        serializer_class = PostSerializer(self.queryset, many=True)

        return Response(serializer_class.data)
    
    def retrive(self, request, pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer_class = PostSerializer(post)

        return Response(serializer_class.data)
    
    def create(self, request):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
BASIC APPROACH


class PostList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
    permission_classes = [PostUserWritePermission]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 CONCRETE VIEW CLSSES


#CreateAPIView
Used for create-only endpoints.
#ListAPIView
Used for read-only endpoints to represent a collection of model instances.
#RetrieveAPIView
Used for read-only endpoints to represent a single model instance.
#DestroyAPIView
Used for delete-only endpoints for a single model instance.
#UpdateAPIView
Used for update-only endpoints for a single model instance.
##ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.
RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.
#RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.
#RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.

When you apply permisson take care what your view can do anyway - i.e:
class PostDetail(generics.RetrieveDestroyAPIView, PostUserWritePermission):
    here you can't update post (even if your custom permission allow to do so), because
    this functionality is not implemented on this view (only Retrieve and Destroy)
"""

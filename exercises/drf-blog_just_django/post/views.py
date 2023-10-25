from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render

from .models import Post, Author
from .serializers import PostSerlializer, PostCreateSeliarizer, AuthorSerializer


def home(request):
    return render(request, "index.html")


def post_detail(request, pk):
    return render(request, "post_detail.html")


class AuthorDetailView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class PostListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PostSerlializer
    queryset = Post.objects.all()


class PostCreateView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PostCreateSeliarizer
    queryset = Post.objects.all()


class PostDetailView(RetrieveAPIView):
    permission_class = (AllowAny,)
    serializer_class = PostSerlializer
    queryset = Post.objects.all()


class PostUpdateView(UpdateAPIView):
    permission_class = (AllowAny,)
    serializer_class = PostCreateSeliarizer
    queryset = Post.objects.all()


class PostDeleteView(DestroyAPIView):
    permission_class = (AllowAny,)
    queryset = Post.objects.all()
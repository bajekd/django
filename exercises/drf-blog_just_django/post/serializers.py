from django.db.models import fields
from rest_framework import serializers

from .models import Post, Author


class AuthorSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ("username",)

    def get_username(self, obj):
        return obj.user.username


class PostSerlializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "author", "title", "content", "publish_date", "updated")


class PostCreateSeliarizer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "content", "author")

from rest_framework import serializers

from blog.apps.blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "author", "category", "excerpt", "slug", "content", "status")

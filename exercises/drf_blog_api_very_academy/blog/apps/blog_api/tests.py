from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blog.apps.blog.models import Category, Post


class PostTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name="test")

        User.objects.create_superuser(username="test__superuser", password="123456789")
        User.objects.create_user(username="test_user_1", password="123456789")
        User.objects.create_user(username="test_user_2", password="123456789")

    def test_only_logged_user_can_view_post_list(self):
        url = reverse("blog_api:list_create")

        response_unauthenticated_user = self.client.get(url, format="json")

        self.client.login(username="test_user_2", password="123456789")
        response_authenticated = self.client.get(url, format="json")

        self.assertEqual(response_unauthenticated_user.status_code, 403)
        self.assertEqual(response_authenticated.status_code, 200)

    def test_only_logged_user_can_create_post(self):
        url = reverse("blog_api:list_create")
        data = {"category": 1, "title": "Post Title", "excerpt": "Post Excerpt", "content": "Post Content", 
            "slug": "post-title", "status": "published"}

        response_unauthenticated_user = self.client.post(url, data, format="json")
        
        self.client.login(username="test_user_1", password="123456789")
        data.update(author=2)
        response_authenticated_user = self.client.post(url, data, format="json")

        self.assertEqual(response_unauthenticated_user.status_code, 403)
        self.assertEqual(response_authenticated_user.status_code, 201)

    def test_only_author_can_edit_his_post(self):
        Post.objects.create(
            category_id=1,
            title="Post Title",
            excerpt="Post Excerpt",
            content="Post Content",
            slug="post-title",
            author_id=3,
            status="published",
        )
        url = reverse("blog_api:detail_edit_delete", kwargs={"pk": 1})

        response_unauthenticated_user = self.client.patch(url, {}, format="json")

        self.client.login(username="test_user_1", password="123456789")
        response_logged_user_but_not_author = self.client.patch(url, {}, format="json")

        self.client.login(username="test_user_2", password="123456789")
        response_author = self.client.patch(url, {}, format="json")

        self.assertEqual(response_unauthenticated_user.status_code, 403)
        self.assertEqual(response_logged_user_but_not_author.status_code, 403)
        self.assertEqual(response_author.status_code, 200)

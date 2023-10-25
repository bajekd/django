from django.contrib.auth import get_user_model
from django.test import TestCase

from blog.apps.blog.models import Category, Post


class Test_Create_Post(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model()
        Category.objects.create(name="test")
        user.objects.create_user(email="test_user@test.com", password="123456789")
        Post.objects.create(
            category_id=1,
            title="Post Title",
            excerpt="Post Excerpt",
            content="Post Content",
            slug="post-title",
            author_id=1,
            status="published",
        )

    def test_blog_content(self):
        post = Post.objects.get(id=1)
        category = Category.objects.get(id=1)
        author = f"{post.author}"
        post_title = f"{post.title}"
        post_excerpt = f"{post.excerpt}"
        post_content = f"{post.content}"
        post_status = f"{post.status}"

        self.assertEqual(author, "test_user@test.com")
        self.assertEqual(post_title, "Post Title")
        self.assertEqual(post_excerpt, "Post Excerpt")
        self.assertEqual(post_content, "Post Content")
        self.assertEqual(post_status, "published")
        self.assertEqual(str(post), "Post Title")
        self.assertEqual(str(category), "test")

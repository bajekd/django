from django.urls import path
from django.urls.conf import include

from .views import AuthorDetailView, PostListView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView

app_name = "posts"

urlpatterns = [
    path("author/<pk>/", AuthorDetailView.as_view(), name="author_list"),
    path("", include([
        path("", PostListView.as_view(), name="post_list"),
        path("create/", PostCreateView.as_view(), name="post_create"),
        path("<pk>/", PostDetailView.as_view(), name="post_detail"),
        path("<pk>/update/", PostUpdateView.as_view(), name="post_update"),
        path("<pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    ])),
]

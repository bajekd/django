from rest_framework.routers import DefaultRouter

from .views import PostList

app_name = "blog_api"

router = DefaultRouter()
router.register("", PostList, basename="post")
urlpatterns = router.urls


"""
from django.urls import include, path

from .views import PostDtail, PostList


urlpatterns = [
   
    path('', PostList.as_view(), name='list_create'),
    path('<int:pk>/', PostDetail.as_view(), name='detail_edit_delete'),
    
    ])), 
]
"""
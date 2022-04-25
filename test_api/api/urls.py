from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, PostCommentViewSet


router = DefaultRouter()
router.register('posts', PostViewSet)
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    PostCommentViewSet,
    basename='comments_to_post'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
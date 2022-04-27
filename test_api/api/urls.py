from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AddCommentView, PostCommentViewSet, PostViewSet, NestedCommentsView

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    PostCommentViewSet,
    basename='comments_to_post'
)


urlpatterns = [
    path('', include(router.urls)),
    path(
        'posts/<int:post_id>/comments/<int:comment_id>/add_comment/',
        AddCommentView.as_view()),
    path(
        'posts/<int:post_id>/comments/<int:comment_id>/nested/',
        NestedCommentsView.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

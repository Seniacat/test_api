from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets

from api.models import Comment, Post
from api.permissions import IsAuthorOrReadOnly
from api.serializers import AddCommentSerializer, PostSerializer


class ListCreateDestroyViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):

    pass


User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """Cтатьи блога"""

    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostCommentViewSet(ListCreateDestroyViewSet):
    """Комментарии к статье"""
    serializer_class = AddCommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(
            Post.objects.prefetch_related('comments'),
            pk=post_id
        )
        queryset = Comment.objects.select_related(
            'author', 'post', 'post__author').filter(
            post=post,
            level__lte=settings.MAX_NESTED_LEVEL
        )
        return queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(
            author=self.request.user,
            post=post
        )


class CommentViewSet(PostCommentViewSet):
    """Вложенные комментарии
    к комментариям верхнего уровня"""
    def get_queryset(self):
        comment_id = self.kwargs.get('comment_id')
        comment = get_object_or_404(Comment, pk=comment_id)
        comments = Comment.objects.select_related(
            'author', 'post', 'post__author'
            ).filter(parent=comment)
        return comments

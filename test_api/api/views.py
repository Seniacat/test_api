from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.models import Comment, Post
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (AddCommentSerializer, CommentSerializer,
                             PostCommentSerializer, PostSerializer)


class ListCreateDestroyViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):

    pass


User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """Cтатьи блога.
    Получение списка статей и добавление новой статьи.
    """

    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostCommentViewSet(ListCreateDestroyViewSet):
    """Комментарии к статье.
    Получение списка всех комментариев к статье
    до 3го уровня вложенности, а также добавления
    комментариев к статье.
    """
    serializer_class = PostCommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        post_id = int(self.kwargs.get('post_id'))
        queryset = Comment.objects.filter(
            post__id=post_id,
            level__lte=settings.MAX_NESTED_LEVEL
        ).select_related(
            'author', 'post', 'post__author'
        )
        return queryset

    def perform_create(self, serializer):
        post_id = int(self.kwargs.get('post_id'))
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(
            author=self.request.user,
            post=post
        )


class AddCommentView(generics.CreateAPIView):
    """Добавление комментариев к комментариям верхнего уровня."""
    serializer_class = AddCommentSerializer
    permission_classes = (IsAuthenticated,)


class NestedCommentsView(generics.ListAPIView):
    """Получение вложенных комментариев к комментариям 3го уровня"""
    serializer_class = CommentSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        comment_id = self.kwargs.get('comment_id')
        comments = Comment.objects.filter(
            main_parent_id=comment_id).select_related(
            'author', 'post', 'post__author', 'main_parent'
        )
        return comments

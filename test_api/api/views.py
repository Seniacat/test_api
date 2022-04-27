from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.models import Comment, Post
from api.permissions import IsAuthorOrReadOnly
from api.serializers import AddCommentSerializer, CommentSerializer, PostSerializer, PostCommentSerializer


class ListCreateDestroyViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):

    pass


User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """Cтатьи блога
    Получение списка статей и добавление новой статьи
    """

    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostCommentViewSet(ListCreateDestroyViewSet):
    """Комментарии к статье.
    Формирует queryset из всех комментариев к статье
    до 3го уровня вложенности, а также добавляет комментарии к статье    
    """
    serializer_class = PostCommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        post_id = int(self.kwargs.get('post_id'))
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
        post_id = int(self.kwargs.get('post_id'))
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(
            author=self.request.user,
            post=post
        )


class AddCommentView(generics.CreateAPIView):
    """Добавление комментариев к комментариям верхнего уровня"""
    serializer_class = AddCommentSerializer
    permission_classes = (IsAuthenticated,)

    
class NestedCommentsView(generics.ListAPIView):
    """Получение вложенных комментариев для комментариям 3го уровня"""
    serializer_class = CommentSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        comment_id = self.kwargs.get('comment_id')
        comment = get_object_or_404(Comment, pk=comment_id)
        comments = Comment.objects.select_related('author').filter(main_parent=comment)
        return comments
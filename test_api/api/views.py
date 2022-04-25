from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, viewsets

from api.models import Comment, Post
from api.serializers import PostSerializer, CommentSerializer


class ListCreateDestroyViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):

    pass

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostCommentViewSet(ListCreateDestroyViewSet):
    serializer_class = CommentSerializer
    # permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(
            Post.objects.select_related('author').prefetch_related('comments'),
            pk=post_id)
        queryset = Comment.objects.filter(
            post=post,
            level__lte=settings.MAX_NESTED_LEVEL
        )
        return queryset

    def perform_create(self, serializer):
        post_id = int(self.kwargs.get('post_id'))
        get_object_or_404(Post, pk=post_id)
        serializer.save(
            author=self.request.user,
            post_id=post_id
        )
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from requests import request
from rest_framework import serializers

from api.models import Comment, Post

User = get_user_model()


class AddPostSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления статей в блог"""

    class Meta:
        fields = ('name', 'text')
        model = Post

    def to_representation(self, instance):
        serializer = PostSerializer(instance)
        return serializer.data


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения статьи блога"""

    author = UserSerializer(read_only=True)

    class Meta:
        fields = ('id', 'author', 'name', 'text', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения комментариев"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = (
            'id',
            'author',
            'text',
            'level',
            'created',
            'parent',
            'post'
        )
        model = Comment


class PostCommentSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления комментариев к постам"""

    class Meta:
        fields = ('text',)
        model = Comment

    def to_representation(self, instance):
        serializer = CommentSerializer(instance)
        return serializer.data


class AddCommentSerializer(PostCommentSerializer):
    """Сериализатор для добавления комментариев
        к комментариям верхнего уровня"""

    def create(self, validated_data):
        request = self.context.get('request')
        parent_id = self.context.get('view').kwargs.get('comment_id')
        post_id = self.context.get('view').kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        parent = get_object_or_404(Comment, pk=parent_id)
        comment = Comment.objects.create(
            **validated_data,
            post=post,
            parent=parent,
            author = request.user
        )
        comment.level = parent.level + 1
        if parent.level == 3:
            comment.main_parent = parent
        elif parent.level > 3:
            comment.main_parent = parent.main_parent
        comment.save()
        return comment

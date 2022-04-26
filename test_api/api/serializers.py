from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.models import Comment, Post

User = get_user_model()


class AddPostSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'text')
        model = Post

    def to_representation(self, instance):
        serializer = PostSerializer(instance)
        return serializer.data    
 

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        fields = ('id', 'author', 'name', 'text', 'pub_date')
        model = Post


class AddCommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('text',)
        model = Comment

    def to_representation(self, instance):
        serializer = CommentSerializer(instance)
        return serializer.data

    def create(self, validated_data):
        parent_id = self.context.get('view').kwargs.get('comment_id')
        comment = Comment.objects.create(**validated_data)
        if parent_id:
            parent = get_object_or_404(
                Comment,
                pk=parent_id
            )
            comment.level = parent.level + 1
            comment.parent = parent
            comment.save()
        return comment


class CommentSerializer(serializers.ModelSerializer):
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

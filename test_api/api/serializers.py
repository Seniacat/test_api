from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.models import Comment, Post

User = get_user_model()


"""class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'first_name',
            'last_name',
            'email'
        )"""

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


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = (
            'id',
            'author',
            'text',
            'level',
            'created',
            'parent_id',
            'post'
        )
        model = Comment

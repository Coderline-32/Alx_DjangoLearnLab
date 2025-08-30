from rest_framework import serializers
from .models import Post, Comment
from django.conf import settings

User = settings.AUTH_USER_MODEL

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'author_username', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        return super().create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author_username', 'title', 'content', 'created_at', 'updated_at', 'comments']
        read_only_fields = ['id', 'author_username', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        return super().create(validated_data)

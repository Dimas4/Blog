from rest_framework import serializers

from post.models import Posts


class PostsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = (
            'title',
            'content',
            'category',
            'image'
        )


class PostsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = (
            'title',
            'content'
        )


class PostsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = (
            'title',
            'content',
            'rate',
            'views'
        )

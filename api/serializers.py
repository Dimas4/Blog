from rest_framework import serializers
from post.models import Posts
from chat_message.models import Messages


class PostsSerializer(serializers.ModelSerializer):
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


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    author_profile = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Messages
        fields = (
            'author',
            'author_profile',
            'content',
        )



class MessageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = (
            'content',
        )

from rest_framework import serializers

from chat_message.models import Messages


class MessageSerializer(serializers.ModelSerializer):
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

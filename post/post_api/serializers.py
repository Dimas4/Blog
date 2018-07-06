from rest_framework import serializers

from post.models import Posts


class PostsCreateSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Posts
        fields = [
            'url',
            'title',
            'content',
            'category',
            'image',
        ]
        read_only_fields = ['url']

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)


class PostsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = (
            'title',
            'content',
            'rate',
            'views'
        )
        read_only_fields = ['rate', 'views']

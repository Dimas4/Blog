from rest_framework import serializers
from post.models import Posts


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ('title', 'content')

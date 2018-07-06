from django.db.models import Q

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics
from rest_framework import mixins

from .serializers import (
    PostsDetailSerializer,
    PostsCreateSerializer
    )
from post.models import Posts


class PostListAPIView(mixins.CreateModelMixin,
                      generics.ListAPIView):
    serializer_class = PostsCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Posts.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(title__icontains=query)).distinct()
        return qs

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def get_serializer_context(self, *args, **kwargs):
    #     return {"request": self.request}


class PostDetailAPIView(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from post.models import Posts
from chat_message.models import Messages
from .serializers import PostsSerializer, PostsDetailSerializer, MessageSerializer, MessageDetailSerializer
from rest_framework.decorators import api_view
from rest_framework import status, permissions
from rest_framework.views import APIView
from .permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework.generics import CreateAPIView

# def allow_method(arg):
#     def wrap(func):
#         def inner(request):
#             if request.method not in arg:
#                 return HttpResponse(status=404)
#             return func(request)
#         return inner
#     return wrap
#
#
# @allow_method(["GET", "POST"])


@api_view(['GET', 'POST'])
def posts_list(request, format=None):

    if request.method == 'GET':
        posts = Posts.objects.all()
        serializer = PostsSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)  # Why i must use this?
        serializer = PostsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk, format=None):

    post = get_object_or_404(Posts, pk=pk)

    if request.method == 'GET':
        serializer = PostsDetailSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostsDetailSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessagesList(APIView):

    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)

    def get(self, request):
        messages = Messages.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessagesDetail(APIView):

    def get_object(self, pk):
        return get_object_or_404(Messages, pk=pk)

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = MessageDetailSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = MessageDetailSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

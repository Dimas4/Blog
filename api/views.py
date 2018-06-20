from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from post.models import Posts
from .serializers import PostsSerializer
from rest_framework.decorators import api_view
from rest_framework import status


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
def posts_list(request):

    if request.method == 'GET':
        posts = Posts.objects.all()
        serializer = PostsSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):

    post = get_object_or_404(Posts, pk=pk)

    if request.method == 'GET':
        serializer = PostsSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostsSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

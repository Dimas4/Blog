from django.contrib.auth.models import User
from django.http import HttpResponse

from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework import generics

from .serializers import UserCreateSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class Register(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password
                                        )
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        token = Token.objects.create(user=user)

        return HttpResponse({'detail': token.key})





































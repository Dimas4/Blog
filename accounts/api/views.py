from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserCreateSerializer


class Register(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.data.get('username')
            email = serializer.data.get('email')
            password = serializer.data.get('password')

            user = User.objects.create_user(username, email, password)
            token = Token.objects.create(user=user)

            context = {
                'key': token.key
            }

            return Response(context)

        return Response(data=serializer.errors)

from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password2 = serializers.CharField(required=True)

    def validate(self, data):
        username = data['username']
        email = data['email']
        password = data['password']
        password2 = data['password2']

        check_username = User.objects.filter(username=username)
        if check_username.exists():
            raise serializers.ValidationError({'username': [
                "A user with that username already exists."
            ]})
            
        check_email = User.objects.filter(email=email)
        if check_email.exists():
            raise serializers.ValidationError({'email': [
                "A user is already registered with this e-mail address."
            ]})

        if password != password2 or len(password) < 8:
            raise serializers.ValidationError({"non_field_errors": [
                "The two password fields didn't match or password len less then 8 characters!"
            ]})

        return data

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
        ]
        extra_kwargs = {"password":
                        {"write_only": True}
                        }

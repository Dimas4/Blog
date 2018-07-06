from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
        ]
        extra_kwargs = {"password":
                        {"write_only": True}
                        }

        def validate_email(self, value):
            data = self.get_initial()
            email1 = data.get("email")
            check_email = User.objects.filter(email=email1)
            if check_email.exists():
                raise serializers.ValidationError("This user has already registered!")
            return value

        def create(self, validate_data):
            username = validate_data['username']
            email = validate_data['email']
            password = validate_data['password']
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            new_user.save()
            return validate_data

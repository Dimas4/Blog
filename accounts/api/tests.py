from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APIClient


class TestAPIViews(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user('admin23', email='admin23@mail.ru', password='admin23admin23')
        self.user.save()
        token = Token.objects.create(user=self.user)
        token.save()

    def test_custom_registration(self):
        request = self.client.post('/api/account/custom_registration/', {'username': 'admin21',
                                                                         'password': 'admin21admin21'})
        self.assertEqual(request.status_code, 200)

    def test_login(self):
        request = self.client.post('/api/account/rest-auth/login/', {'username': 'admin23',
                                                                     'email': 'admin23@mail.ru',
                                                                     'password': 'admin23admin23'})

        self.assertEqual(request.status_code, 200)

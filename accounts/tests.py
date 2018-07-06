from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client

from .models import UserProfile


class AccountTest(TestCase):
    def setUp(self):
        user = User.objects.create(username="admin", email="admin@mail.ru", password="adminadmin")
        UserProfile.objects.create(user=user)

    def test_get_user_url(self):
        c = Client()
        response = c.post('/login/', {'username': 'admin', 'password': 'adminadmin'})
        self.assertEqual(response.status_code, 200)

    def test_str(self):
        user = User.objects.get(username="admin", email="admin@mail.ru", password="adminadmin")
        user_profile = UserProfile.objects.get(user=user)
        self.assertEqual(user.__str__(), user_profile.user.username)

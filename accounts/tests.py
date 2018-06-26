from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client


class AccountTest(TestCase):
    def setUp(self):
        User.objects.create(username="admin", email="admin@mail.ru", password="adminadmin")

    def test_get_user_url(self):

        c = Client()
        response = c.post('/login/', {'username': 'admin', 'password': 'adminadmin'})
        self.assertEqual(response.status_code, 200)

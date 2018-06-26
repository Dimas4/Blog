from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import UserProfile
from .models import Messages


class PostsTest(TestCase):
    def setUp(self):
        user = User.objects.create(username="admin", email="admin@mail.ru", password="adminadmin")
        user_profile = UserProfile.objects.create(user=user)
        Messages.objects.create(author=user, author_profile=user_profile, content="Content")

    def test_get_user_url(self):
        message = Messages.objects.get(content="Content")
        self.assertEqual(message.get_user_url(), '/account/1/')

from rest_framework.test import RequestsClient
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from post.models import Posts, Category
from accounts.models import UserProfile
from chat_message.models import Messages


class ApiTest(APITestCase):
    def setUp(self):
        category = Category.objects.create(name="First Category", content="mu category content")
        user = User.objects.create(username="admin", email="admin@mail.ru", password="adminadmin")
        user_profile = UserProfile.objects.create(user=user)
        Posts.objects.create(user=user, title="my title", content="my content",
                             rate=5, views=5, category=category)
        Messages.objects.create(author=user, author_profile=user_profile, content="Message")

    def test_get_posts_all(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/posts/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.json()), "[{'title': 'my title', 'content': 'my content'}]")

    def test_get_posts_detail(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/posts/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.json()), "{'title': 'my title', 'content': 'my content',"
                                               " 'rate': 5, 'views': 5}")

    def test_get_messages_all(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/messages/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.json()), "[{'author': 1, 'author_profile': 1, 'content': 'Message'}]")

    def test_get_messages_detail(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/messages/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.json()), "{'content': 'Message'}")

    def test_post_posts(self):
        url = '/login/'
        data = {'username': 'admin', 'password': 'adminadmin'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 200)


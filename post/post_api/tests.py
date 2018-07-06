from django.contrib.auth.models import User

from rest_framework.test import RequestsClient
from rest_framework.test import APITestCase

from chat_message.models import Messages
from post.models import Posts, Category
from accounts.models import UserProfile


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

    def test_get_posts_detail(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/posts/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.json()), "{'title': 'my title', 'content': 'my content',"
                                               " 'rate': 5, 'views': 5}")

    # def test_post_post(self):
    #     client = RequestsClient()
    #     user = User.objects.get(username="admin")
    #     category = Category.objects.get(name="First Category")
    #
    #     self.client.login(username='admin', password='adminadmin')
    #     post = self.client.post('http://127.0.0.1:8000/api/posts/', {'user': user, 'title': 'my title',
    #                                                                  'content': 'my content', 'category': category})
    #     print(post)
    #     response = client.get('http://127.0.0.1:8000/api/posts/2')
    #
    #     self.assertEqual(response.status_code, 200)

    def test_post_delete(self):
        client = RequestsClient()
        response = client.delete('http://127.0.0.1:8000/api/posts/1')
        response = client.delete('http://127.0.0.1:8000/api/posts/1')

        self.assertEqual(response.status_code, 404)

    def test_post_posts(self):
        url = '/login/'
        data = {'username': 'admin', 'password': 'adminadmin'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

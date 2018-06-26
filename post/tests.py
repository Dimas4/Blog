from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.test import Client

from .models import Posts, Category
from likes.models import Like

from . import views


class PostsTest(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.category = Category.objects.create(name="First Category", content="mu category content")
        self.user = self.user_model.objects.create(username="admin", email="admin@mail.ru", password="adminadmin")
        self.client.login(username='admin1', password='adminadmin')
        Posts.objects.create(user=self.user, title="my title", content="my content",
                             rate=5, views=5, category=self.category)

    def test_get_user_url(self):
        post = Posts.objects.get(title="my title")
        self.assertEqual(post.get_user_url(), '/account/1/')

    def test_get_absolute_url(self):
        post = Posts.objects.get(title="my title")
        self.assertEqual(post.get_absolute_url(), '/posts/1/')

    def test_edit_post(self):
        post = Posts.objects.get(title="my title")
        self.assertEqual(post.edit_post(), '/posts/1/edit/')

    def test_delete_post(self):
        post = Posts.objects.get(title="my title")
        self.assertEqual(post.delete_post(), '/posts/1/delete/')

    def test_update_view(self):
        post = Posts.objects.get(title="my title")
        self.assertEqual(post.update_view(post.id).views, 6)

    def test_like_cont(self):
        post = Posts.objects.get(title="my title")
        self.assertEqual(post.total_likes, 0)

    def test_is_liked_false(self):
        post = Posts.objects.get(title="my title")
        user = User.objects.get(username="admin", email="admin@mail.ru", password="adminadmin")
        self.assertEqual(post.is_like(user), False)

    def test_is_liked_true(self):
        obj_type = ContentType.objects.get_for_model(Posts)
        post = Posts.objects.get(title="my title")
        user = User.objects.get(username="admin", email="admin@mail.ru", password="adminadmin")
        Like.objects.create(content_type=obj_type, object_id=post.id, user=user)
        self.assertEqual(post.is_like(user), True)

    def test_manager_rate(self):
        category = Category.objects.get(name="First Category", content="mu category content")
        post = Posts.objects.get(title="my title")

        post_l = Posts.objects.create(user=self.user, title="1title", content="1my content",
                                      rate=5, views=5, category=category)
        post_m = Posts.objects.create(user=self.user, title="2title", content="2my content",
                                      rate=10, views=5, category=category)
        post_h = Posts.objects.create(user=self.user, title="3title", content="3my content",
                                      rate=50, views=5, category=category)

        self.assertEqual(Posts.objects.low_rate()[0], post)
        self.assertEqual(Posts.objects.low_rate()[1], post_l)
        self.assertEqual(Posts.objects.middle_rate()[0], post_m)
        self.assertEqual(Posts.objects.high_rate()[0], post_h)

    def test_category_str(self):
        category = Category.objects.get(name="First Category")

        self.assertEqual(category.__str__(), category.name)

    def test_post_str(self):
        post = Posts.objects.get(title="my title")
        self.assertEqual(post.__str__(), post.title)

    def test_view_create_page(self):
        self.user_model.objects.create_user('admin1', 'admin@gmail.com', 'adminadmin')
        self.client.login(username='admin1', password='adminadmin')

        response = self.client.get(reverse('post:create_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/create_page.html')

    def test_view_category_detail(self):
        category = Category.objects.create(name='test_category', content='test')

        post = Posts.objects.create(user=self.user, title="my title", content="my content",
                             rate=5, views=5, category=category)

        response = self.client.get(reverse('post:category_detail_view', kwargs={'slug': 'test_category'}))

        self.assertEqual(response.context['posts'][0], post)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/category.html')

    def test_view_edit_page(self):
        user = self.user_model.objects.create_user('admin1', 'admin@gmail.com', 'adminadmin')
        self.client.login(username='admin1', password='adminadmin')

        post = Posts.objects.create(user=user, title="aaaaamy title", content="my content",
                                    rate=10, views=10, category=self.category)

        response = self.client.get(reverse('post:edit_page', kwargs={'id': post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/edit_page.html')

    def test_view_delete_page(self):
        user = self.user_model.objects.create_user('admin1', 'admin1@gmail.com', 'adminadmin')
        self.client.login(username='admin1', password='adminadmin')

        post = Posts.objects.create(user=user, title="my title delete", content="my content",
                                    rate=10, views=10, category=self.category)

        response = self.client.post(reverse('post:delete_page', kwargs={'id': post.id}))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'home/delete_page.html')

    def test_view_like(self):
        self.client.login(username='admin1', password='adminadmin')

        model_type = ContentType.objects.get_for_model(Posts)
        post = Posts.objects.create(user=self.user, title="my title delete", content="my content",
                                    rate=10, views=10, category=self.category)

        Like.objects.create(content_type=model_type, object_id=post.id, user=self.user)

        obj = Like.objects.filter(content_type=model_type, object_id=post.id, user=self.user)

        self.assertEqual(len(obj), 1)

    def test_view_like_add(self):

        model_type = ContentType.objects.get_for_model(Posts)
        post = Posts.objects.create(user=self.user, title="my title delete", content="my content",
                                    rate=10, views=10, category=self.category)

        Like.objects.create(content_type=model_type, object_id=post.id, user=self.user)
        obj = Like.objects.filter(content_type=model_type, object_id=post.id, user=self.user)

        self.assertEqual(len(obj), 1)

        Like.objects.create(content_type=model_type, object_id=post.id, user=self.user)
        obj = Like.objects.filter(content_type=model_type, object_id=post.id, user=self.user)

        self.assertEqual(len(obj), 2)

    def test_view_rate(self):
        post_h = Posts.objects.create(user=self.user, title="my title delete", content="my content",
                                      rate=50, views=10, category=self.category)

        post_m = Posts.objects.create(user=self.user, title="my title delete", content="my content",
                                      rate=15, views=10, category=self.category)

        post_l = Posts.objects.create(user=self.user, title="my title delete", content="my content",
                                      rate=2, views=10, category=self.category)

        response = self.client.post(reverse('post:high_middle_low_rate', kwargs={'slug': 'high_rate'}))

        self.assertEqual(response.context['posts'][0], post_h)

        response = self.client.post(reverse('post:high_middle_low_rate', kwargs={'slug': 'middle_rate'}))
        self.assertEqual(response.context['posts'][0], post_m)

        response = self.client.post(reverse('post:high_middle_low_rate', kwargs={'slug': 'low_rate'}))
        self.assertEqual(response.context['posts'][1], post_l)



from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.test import TestCase


from .models import Posts, Category
from likes.models import Like


class PostsTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name="First Category", content="mu category content")
        user = User.objects.create(username="admin", email="admin@mail.ru", password="adminadmin")
        Posts.objects.create(user=user, title="my title", content="my content",
                             rate=5, views=5, category=category)

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
        user = User.objects.get(username="admin", email="admin@mail.ru", password="adminadmin")
        category = Category.objects.get(name="First Category", content="mu category content")
        post = Posts.objects.get(title="my title")

        post_l = Posts.objects.create(user=user, title="1title", content="1my content",
                                      rate=5, views=5, category=category)
        post_m = Posts.objects.create(user=user, title="2title", content="2my content",
                                      rate=10, views=5, category=category)
        post_h = Posts.objects.create(user=user, title="3title", content="3my content",
                                      rate=50, views=5, category=category)

        self.assertEqual(Posts.objects.low_rate()[0], post)
        self.assertEqual(Posts.objects.low_rate()[1], post_l)
        self.assertEqual(Posts.objects.middle_rate()[0], post_m)
        self.assertEqual(Posts.objects.high_rate()[0], post_h)

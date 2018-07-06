from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.test import TestCase

from post.models import Posts, Category
from .models import Like


class CommentsTest(TestCase):
    def setUp(self):
        user = User.objects.create(username="admin", email="admin@mail.ru", password="adminadmin")
        category = Category.objects.create(name="First Category", content="mu category content")

        post = Posts.objects.create(user=user, title="my title", content="my content",
                                    rate=5, views=5, category=category)

        obj_type = ContentType.objects.get_for_model(Posts)

        Like.objects.create(content_type=obj_type, object_id=post.id,
                            user=user)

    def test_exists(self):
        user = User.objects.get(username="admin")

        like = Like.objects.get(user=user)

        self.assertEqual(Like.objects.all().first(), like)

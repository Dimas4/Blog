from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.test import TestCase

from .models import Comments
from post.models import Posts, Category
from accounts.models import UserProfile


class CommentsTest(TestCase):
    def setUp(self):
        user = User.objects.create(username="admin", email="admin@mail.ru", password="adminadmin")
        category = Category.objects.create(name="First Category", content="mu category content")

        post = Posts.objects.create(user=user, title="my title", content="my content",
                                    rate=5, views=5, category=category)

        userprofile = UserProfile.objects.create(user=user)

        obj_type = ContentType.objects.get_for_model(Posts)

        Comments.objects.create(content_type=obj_type, object_id=post.id,
                                user=user, userprofile=userprofile)

    def test_get_user_url(self):
        user = User.objects.get(username="admin")

        comment = Comments.objects.get(user=user)

        self.assertEqual(comment.get_user_url(), '/account/1/')

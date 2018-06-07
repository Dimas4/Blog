from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.urls import reverse

from likes.models import Like
from django.db import models


class PostManager(models.Manager):
    def high_rate(self, *args, **kwargs):
        return Posts.objects.filter(rate__range=(25, 101))

    def middle_rate(self, *args, **kwargs):
        return Posts.objects.filter(rate__range=(5, 25))

    def low_rate(self, *args, **kwargs):
        return Posts.objects.filter(rate__range=(0, 5))


def generate_image_path(instance, filename):
    filename = instance.id
    return "{directory}/{file}".format(directory=instance.id//7, file=filename)


# def upload_location(instance, filename):
#     PostModel = instance.__class__
#     new_id = PostModel.objects.order_by("id").last().id + 1
#     return "%s/%s" % (new_id, filename)


class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()

    image = models.ImageField(upload_to='media',
                              null=True,
                              blank=True,
                             )

    # height_field = models.IntegerField(default=0)
    # width_field = models.IntegerField(default=0)

    rate = models.IntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    objects = PostManager()

    likes = GenericRelation(Like)

    def get_user_url(self):
        return reverse("accounts:account", kwargs={"id": self.user.id})

    def get_absolute_url(self):
        return reverse("post:detail_page", kwargs={"id": self.id})

    def edit_post(self):
        return reverse("post:edit_page", kwargs={"id": self.id})

    def delete_post(self):
        return reverse("post:delete_page", kwargs={"id": self.id})

    @property
    def total_likes(self):
        return self.likes.count()

    def is_like(self, user):
        if not user.is_authenticated:
            return False
        obj_type = ContentType.objects.get_for_model(self)
        likes = Like.objects.filter(content_type=obj_type, object_id=self.id, user=user)
        return likes.exists()

    def __str__(self):
        return self.title


# def pre_save_post_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = create_slug(instance)
#
#     if instance.content:
#         html_string = instance.get_markdown()
#         read_time_var = get_read_time(html_string)
#         instance.read_time = read_time_var
#
#
# pre_save.connect(pre_save_post_receiver, sender=Post)

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import F
from django.db import models
import math

from comments.models import Comments
from likes.models import Like



def content_type_queryset(model, content_type, id):
    return model.objects.filter(content_type=content_type, object_id=id).order_by("-timestamp")


class PostManager(models.Manager):
    def home(self):
        res = []
        posts = self.select_related("category", "user").all().order_by('-timestamp')
        for p in posts:
            if len(res) == 0:
                res.append(p)

            if res[-1].category != p.category:
                res.append(p)

        return res

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


class Category(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(upload_to='media',
                              null=True,
                              blank=True,
                              )

    def __str__(self):
        return self.name


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

    rate = models.PositiveSmallIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    objects = PostManager()

    likes = GenericRelation(Like)

    def get_user_url(self):
        return reverse("accounts:account", kwargs={"id": self.user_id})

    def get_absolute_url(self):
        return reverse("post:detail_page", kwargs={"id": self.id})

    def edit_post(self):
        return reverse("post:edit_page", kwargs={"id": self.id})

    def delete_post(self):
        return reverse("post:delete_page", kwargs={"id": self.id})

    def update_view(self, id):
        self.rate = math.ceil(self.total_likes / (self.views + 1))
        self.views = F('views') + 1
        self.save(update_fields=('views',))
        post = Posts.objects.get(id=id)
        return post

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

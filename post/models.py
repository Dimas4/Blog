from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from django.db.models.signals import pre_save



class PostManager(models.Manager):
    def high_rate(self, *args, **kwargs):
        return super(PostManager, self).filter(rate >= 50)

    def middle_rate(self, *args, **kwargs):
        return super(PostManager, self).filter(rate < 50 and rate >= 10 )

    def low_rate(self, *args, **kwargs):
        return super(PostManager, self).filter(rate < 10)


class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    rate = models.IntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    objects = PostManager()

    def get_absolute_url(self):
        return reverse("post:detail_page", kwargs={"id": self.id})

    def edit_post(self):
        return reverse("post:edit_page", kwargs={"id": self.id})

    def delete_post(self):
        return reverse("post:delete_page", kwargs={"id": self.id})

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

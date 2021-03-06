from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media',
                              null=True,
                              blank=True,
                              default='media/social.jpg'
                              )
    # 'effects.Effect', through = 'ItemEffect', blank = True
    favorite_posts = models.ManyToManyField('post.Posts', blank=True)

    class Meta:
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'

    def get_user_url(self):
        return reverse("accounts:account", kwargs={"id": self.user_id})

    def __str__(self):
        return self.user.username

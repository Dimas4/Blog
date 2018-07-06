from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models

from accounts.models import UserProfile


class Messages(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def get_user_url(self):
        return reverse("accounts:account", kwargs={"id": self.author_id})

    def __str__(self):
        return self.content

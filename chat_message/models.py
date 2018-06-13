from django.db import models
from django.contrib.auth.models import User


class Messages(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

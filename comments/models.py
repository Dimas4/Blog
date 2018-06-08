from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts.models import UserProfile


User = get_user_model()


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_obj = GenericForeignKey('content_type', 'object_id')

    timestamp = models.DateTimeField(auto_now_add=True)

    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def get_user_url(self):
        return reverse("accounts:account", kwargs={"id": self.user.id})

    def __str__(self):
        return self.content

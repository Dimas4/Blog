from django.db import models
from django.contrib.auth.models import User


from post.models import Posts


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Posts)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()

    def __str__(self):
        return self.user.username

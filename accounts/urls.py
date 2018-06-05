from django.urls import path, re_path
from .views import account


urlpatterns = [
    re_path('^(?P<id>\d+)/$', account, name='account'),
]

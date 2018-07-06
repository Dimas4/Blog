from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, re_path

from . import views

app_name = 'post-api'

urlpatterns = [
    path('', views.PostListAPIView.as_view(), name='main'),
    re_path(r'^(?P<pk>[0-9]+)/$', views.PostDetailRUDApiView.as_view(), name='detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

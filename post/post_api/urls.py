from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, re_path

from . import views


urlpatterns = [
    path('', views.PostListAPIView.as_view(), name='main'),
    re_path(r'^(?P<pk>[0-9]+)/$', views.PostDetailAPIView.as_view(), name='detail'),
    re_path(r'^(?P<pk>[0-9]+)/edit$', views.PostDetailAPIView.as_view(), name='edit'),
    re_path(r'^(?P<pk>[0-9]+)/delete$', views.PostDetailAPIView.as_view(), name='delete'),

]

urlpatterns = format_suffix_patterns(urlpatterns)

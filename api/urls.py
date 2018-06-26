from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('posts/', views.posts_list),
    re_path(r'^posts/(?P<pk>[0-9]+)/$', views.post_detail),

    path('messages/', views.MessagesList.as_view()),
    re_path(r'^messages/(?P<pk>[0-9]+)/$', views.MessagesDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

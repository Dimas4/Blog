from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, re_path

from . import views


app_name = 'chat_message-api'

urlpatterns = [
    path('', views.MessagesList.as_view()),
    re_path(r'^(?P<pk>[0-9]+)/$', views.MessagesDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

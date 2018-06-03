from django.contrib import admin
from django.urls import path, re_path, include
from .views import home_page, detail_page, edit_page, delete_page, create_post

urlpatterns = [
    path('', home_page, name='home_page'),
    path('create/', create_post, name='create_post'),
    re_path('^(?P<id>\d+)/$', detail_page, name='detail_page'),
    re_path('^(?P<id>\d+)/edit/$', edit_page, name='edit_page'),
    re_path('^(?P<id>\d+)/delete/$', delete_page, name='delete_page'),
]

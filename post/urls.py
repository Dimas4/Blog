from django.contrib import admin
from django.urls import path, re_path, include
from .views import (
    home_page,
    detail_page,
    edit_page,
    delete_page,
    create_post,
    like_page,
    high_rate,
    middle_rate,
    low_rate
    )

urlpatterns = [
    path('', home_page, name='home_page'),

    path('high/', high_rate, name='high_rate'),
    path('middle/', middle_rate, name='middle_rate'),
    path('low/', low_rate, name='low_rate'),

    path('create/', create_post, name='create_post'),
    re_path('^(?P<id>\d+)/$', detail_page, name='detail_page'),
    re_path('^(?P<id>\d+)/like$', like_page, name='like_page'),
    re_path('^(?P<id>\d+)/edit/$', edit_page, name='edit_page'),
    re_path('^(?P<id>\d+)/delete/$', delete_page, name='delete_page'),
]

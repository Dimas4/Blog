from django.contrib import admin
from django.urls import path, re_path, include
from .views import (
    home_page,
    detail_page,
    edit_page,
    delete_page,
    create_post,
    like_page,
    high_middle_low_rate,
    dynamic_image,
    category_view,
    category_detail_view
    # high_rate,
    # middle_rate,
    # low_rate
    )

urlpatterns = [
    path('', home_page, name='home_page'),
    re_path('^rate/(?P<slug>[-\w]+)/$', high_middle_low_rate, name='high_middle_low_rate'),
    path('category/', category_view, name='category_view'),
    re_path('^category/(?P<slug>[-\w]+)/$', category_detail_view, name='category_detail_view'),
    path('create/', create_post, name='create_post'),
    path('show_post_image/', dynamic_image, name='dynamic_image'),
    re_path('^(?P<id>\d+)/$', detail_page, name='detail_page'),
    re_path('^(?P<id>\d+)/like$', like_page, name='like_page'),
    re_path('^(?P<id>\d+)/edit/$', edit_page, name='edit_page'),
    re_path('^(?P<id>\d+)/delete/$', delete_page, name='delete_page'),
]

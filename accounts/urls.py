from django.urls import path, re_path

from .views import account_home, account_change_profile, change_password


urlpatterns = [
    path('edit/', account_change_profile, name='account_change_profile'),
    path('change_password/', change_password, name='change_password'),
    re_path('^(?P<id>\d+)/$', account_home, name='account'),
]

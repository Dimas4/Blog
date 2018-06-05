from django.urls import path, re_path
from .views import account_home, account_change_profile


urlpatterns = [
    path('edit/', account_change_profile, name='account_change_profile'),
    re_path('^(?P<id>\d+)/$', account_home, name='account'),
]

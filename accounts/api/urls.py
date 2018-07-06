from django.urls import include, path
from .views import Register

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('custom_registration/', Register.as_view()),
    path('', include('django.contrib.auth.urls')),
]

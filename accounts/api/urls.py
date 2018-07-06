from django.urls import include, path
from .views import UserCreateAPIView

urlpatterns = [
    # path('users/', include('users.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    # path('registr/', view = views.Register.as_view()),
    path('', include('django.contrib.auth.urls')),
    path('register/', UserCreateAPIView.as_view(), name='register')
]

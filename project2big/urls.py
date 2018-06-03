from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from accounts.views import login_view, logout_view, register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('register/', register_view, name='register_view'),
    path('post/', include(('post.urls', 'post'), namespace='post')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

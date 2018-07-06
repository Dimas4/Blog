from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib import admin

from accounts.views import login_view, logout_view, register_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('start.urls', 'start'), namespace='start')),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('register/', register_view, name='register_view'),
    path('posts/', include(('post.urls', 'post'), namespace='post')),
    path('account/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('chat/', include(('chat_message.urls', 'chat_message'), namespace='chat_message')),
    path('api-auth/', include('rest_framework.urls')),

    path('api/posts/', include('post.post_api.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

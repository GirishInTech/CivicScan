from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from homepage.views import custom_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('reports/', include('reports.urls')),
    path('logout/', custom_logout, name='logout'),
]

# ✅ Serve media files only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

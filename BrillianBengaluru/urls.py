from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from homepage.views import custom_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),  # 👈 This line shows homepage at root
    path('users/', include('users.urls')),     # your app's urls
    path('accounts/', include('django.contrib.auth.urls')),  # ✅ add this
    path('reports/', include('reports.urls')),  # <-- Ensure this line is here
    path('logout/', custom_logout, name='logout'),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

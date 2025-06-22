from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from homepage.views import custom_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('reports/', include('reports.urls')),
    path('logout/', custom_logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # 🚨 Add only if you really need catch-all for development
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]

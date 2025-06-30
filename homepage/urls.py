from django.urls import path
from . import views
from .views import health_check

urlpatterns = [
    path('', views.home, name='home'),
    path("healthz", health_check, name="healthz"),
    path('offline/', views.offline, name='offline'),
]

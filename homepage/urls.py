from django.urls import path
from . import views
from .views import health_check, debug_nav

urlpatterns = [
    path('', views.home, name='home'),
    path("healthz", health_check, name="healthz"),
    path("debug-nav/", debug_nav, name="debug_nav"),
]

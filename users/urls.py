from django.urls import path
from django.contrib.auth.views import LoginView
from . import views



urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('report/<int:report_id>/', views.report_detail, name='user_report_detail'),
    path('report/<int:report_id>/edit/', views.edit_report, name='edit_report'),
    path('report/<int:report_id>/delete/', views.delete_report, name='delete_report'),
    path('api/check-updates/', views.check_report_updates, name='check_report_updates'),
    # other urls...
]


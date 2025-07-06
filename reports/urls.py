from django.urls import path
from django.shortcuts import render
from .views import hotspot_data
from . import views

urlpatterns = [
    path('submit/', views.submit_report, name='submit_report'),
    path('success/', lambda request: render(request, 'reports/success.html'), name='submit_success'),
    path('my-reports/', views.my_reports, name='my_reports'),  # <-- Add this
    path('data/', views.report_data_json, name='report_data_json'),
    path('map/', views.report_map_view, name='report_map'),
    path('hotspots/data/', hotspot_data, name='hotspot_data'),
    
]


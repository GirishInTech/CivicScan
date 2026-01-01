from django.shortcuts import render, redirect
from .forms import ReportForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Report
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
from django.http import JsonResponse
from .models import Hotspot
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib import messages


# helper function for reverse geocoding with retry to avoid timeouts
geolocator = Nominatim(user_agent="brillianbengaluru")
 
def get_address(lat, lng, retries=3):
    try:
        location = geolocator.reverse((lat, lng), exactly_one=True, timeout=10)
        if location:
            return location.address
        else:
            return "Address not found"
    except GeocoderTimedOut:
        if retries > 0:
            time.sleep(1)
            return get_address(lat, lng, retries - 1)
        else:
            return "Address not found"
    except Exception:
        return "Address not found"


from django.shortcuts import render
from .forms import ReportForm
from .models import Report
from .views import get_address  # Make sure this is imported properly






def submit_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)

            # Attach user if logged in
            if request.user.is_authenticated:
                report.user = request.user

            # Extract lat/lng and reverse geocode
            try:
                lat_str, lng_str = report.location.split(',')
                lat = float(lat_str.strip())
                lng = float(lng_str.strip())
                report.address = get_address(lat, lng)
            except Exception as e:
                report.address = "Address not available"

            report.save()
            print(report.photo.url)  # 👈 this will show us where it got uploaded
            # ✅ Decide which success page to show
            if request.user.is_authenticated:
                return render(request, 'reports/success.html', {'report_id': report.id})
            else:
                return render(request, 'reports/anon_success.html', {'report_id': report.id})
    else:
        form = ReportForm()
        
    
    return render(request, 'reports/submit_report.html', {'form': form})









# def submit_report(request):
#     if request.method == 'POST':
#         form = ReportForm(request.POST, request.FILES)
#         if form.is_valid():
#             report = form.save(commit=False)  # Don't save to DB yet

#             # Attach user if logged in
#             if request.user.is_authenticated:
#                 report.user = request.user

#             # Extract latitude and longitude from location string and get address
#             try:
#                 lat_str, lng_str = report.location.split(',')
#                 lat = float(lat_str.strip())
#                 lng = float(lng_str.strip())
#                 report.address = get_address(lat, lng)  # Reverse geocode
#             except Exception as e:
#                 report.address = "Address not available"

#             report.save()  # Save to DB after setting address
#             return render(request, 'reports/success.html', {'report_id': report.id})
#     else:
#         form = ReportForm()

#     return render(request, 'reports/submit_report.html', {'form': form})


def my_reports(request):
    reports_list = Report.objects.filter(user=request.user).order_by('-submitted_at')
    paginator = Paginator(reports_list, 5)  # Show 5 reports per page

    page_number = request.GET.get('page')
    reports = paginator.get_page(page_number)

    return render(request, 'reports/my_reports.html', {'reports': reports})


def report_data_json(request):
    reports = Report.objects.all()
    data = []
    for report in reports:
        try:
            lat_str, lng_str = report.location.split(',')
            lat = float(lat_str.strip())
            lng = float(lng_str.strip())
        except Exception:
            continue  # skip invalid locations

        data.append({
                'lat': lat,
                'lng': lng,
                'status': report.status,
                'review': report.review,
                'user': report.user.username if report.user else "Anonymous",
                'email': report.user.email if report.user else "N/A",
                'address': report.address or "Address not available",
                'photo_url': report.photo.url if report.photo else None,
                #'photo_url': report.photo.url if report.photo else "",

            })
    return JsonResponse(data, safe=False)


def report_map_view(request):
    return render(request, 'reports/map.html')

def hotspot_data(request):
    hotspots = Hotspot.objects.all()
    data = []

    for hotspot in hotspots:
        data.append({
            'lat': hotspot.latitude,
            'lng': hotspot.longitude,
            'report_count': hotspot.report_count,
            'address': hotspot.address,
        })

    return JsonResponse(data, safe=False)


# Authority Dashboard Views
def is_authority(user):
    """Check if user is part of Authorities group"""
    return user.groups.filter(name='Authorities').exists() or user.is_staff


@user_passes_test(is_authority)
def authority_dashboard(request):
    """Authority dashboard showing all reports with filtering"""
    status_filter = request.GET.get('status', 'all')
    workflow_filter = request.GET.get('workflow', 'all')
    
    reports = Report.objects.all().order_by('submitted_at')  # Changed to ascending order
    
    # Apply filters
    if status_filter != 'all':
        reports = reports.filter(status=status_filter)
    
    if workflow_filter != 'all':
        reports = reports.filter(workflow_status=workflow_filter)
    
    # Pagination
    paginator = Paginator(reports, 10)
    page_number = request.GET.get('page')
    reports = paginator.get_page(page_number)
    
    context = {
        'reports': reports,
        'status_filter': status_filter,
        'workflow_filter': workflow_filter,
        'total_pending': Report.objects.filter(workflow_status='pending').count(),
        'total_under_review': Report.objects.filter(workflow_status='under_review').count(),
        'total_resolved': Report.objects.filter(workflow_status='resolved').count(),
    }
    
    return render(request, 'reports/authority_dashboard.html', context)


@user_passes_test(is_authority)
def report_detail_authority(request, report_id):
    """Detailed view of a report for authority review"""
    report = get_object_or_404(Report, id=report_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        comments = request.POST.get('comments', '')
        
        if action in ['under_review', 'resolved', 'rejected']:
            report.workflow_status = action
            report.reviewed_by = request.user
            report.reviewed_at = timezone.now()
            report.authority_comments = comments
            report.save()
            
            messages.success(request, f'Report status updated to {action.replace("_", " ").title()}')
            return redirect('authority_dashboard')
    
    return render(request, 'reports/report_detail_authority.html', {'report': report})


@user_passes_test(is_authority)
def authority_reports_json(request):
    """JSON endpoint for authority dashboard map view"""
    reports = Report.objects.all()
    data = []
    
    for report in reports:
        try:
            lat_str, lng_str = report.location.split(',')
            lat = float(lat_str.strip())
            lng = float(lng_str.strip())
        except Exception:
            continue
            
        data.append({
            'id': report.id,
            'lat': lat,
            'lng': lng,
            'status': report.status,
            'workflow_status': report.workflow_status,
            'review': report.review,
            'user': report.user.username if report.user else "Anonymous",
            'address': report.address or "Address not available",
            'photo_url': report.photo.url if report.photo else None,
            'submitted_at': report.submitted_at.strftime('%Y-%m-%d %H:%M'),
            'reviewed_by': report.reviewed_by.username if report.reviewed_by else None,
        })
    
    return JsonResponse(data, safe=False)
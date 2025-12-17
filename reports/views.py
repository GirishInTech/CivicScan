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
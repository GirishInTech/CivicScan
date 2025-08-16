from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponse, FileResponse
from django.conf import settings
import os

def home(request):
    return render(request, 'homepage/index.html')  # ✅ m atch this path


def health_check(request):
    return HttpResponse("OK", status=200)


def custom_logout(request):
    logout(request)
    return redirect('home')  # This 'home' must match your homepage URL name

def offline(request):
    """View for the offline page shown when there's no internet connection."""
    return render(request, 'offline.html', status=200)


def service_worker(request):
    """Serve the service worker file with the correct MIME type."""
    sw_path = os.path.join(settings.STATIC_ROOT, 'serviceworker.js')
    response = FileResponse(open(sw_path, 'rb'), content_type='application/javascript')
    response['Service-Worker-Allowed'] = '/'
    return response


def debug_nav(request):
    return render(request, "debug_nav.html")

from django.shortcuts import render


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponse

from django.shortcuts import render

def home(request):
    return render(request, 'homepage/index.html')  # ✅ match this path


def health_check(request):
    return HttpResponse("OK", status=200)


def custom_logout(request):
    logout(request)
    return redirect('home')  # This 'home' must match your homepage URL name



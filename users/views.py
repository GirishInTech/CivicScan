from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from .forms import SignupForm

from django.contrib.auth.decorators import login_required
from reports.models import Report
from .models import UserProfile

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # After signup, redirect to login page
    else:
        form = SignupForm()

    return render(request, 'users/signup.html', {'form': form})



@login_required
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_reports = Report.objects.filter(user=request.user).order_by('-submitted_at')
    
    return render(request, 'users/dashboard.html', {
        'profile': user_profile,
        'reports': user_reports,
    })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .forms import SignupForm

from django.contrib.auth.decorators import login_required
from reports.models import Report
from .models import UserProfile
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

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
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        user_profile = UserProfile.objects.create(
            user=request.user,
            phone_number="N/A"
        )
    
    user_reports = Report.objects.filter(user=request.user).order_by('-submitted_at')
    
    # Calculate statistics for user
    total_reports = user_reports.count()
    pending_reports = user_reports.filter(workflow_status='pending').count()
    under_review_reports = user_reports.filter(workflow_status='under_review').count()
    resolved_reports = user_reports.filter(workflow_status='resolved').count()
    rejected_reports = user_reports.filter(workflow_status='rejected').count()
    
    # Get recent activity (reports with status changes)
    recent_activity = user_reports.exclude(reviewed_at__isnull=True).order_by('-reviewed_at')[:5]
    
    return render(request, 'users/dashboard.html', {
        'profile': user_profile,
        'reports': user_reports,
        'total_reports': total_reports,
        'pending_reports': pending_reports,
        'under_review_reports': under_review_reports,
        'resolved_reports': resolved_reports,
        'rejected_reports': rejected_reports,
        'recent_activity': recent_activity,
    })


@login_required
def report_detail(request, report_id):
    """Detailed view of user's specific report with full status tracking"""
    report = get_object_or_404(Report, id=report_id, user=request.user)
    
    return render(request, 'users/report_detail.html', {
        'report': report,
    })


@login_required 
def check_report_updates(request):
    """API endpoint to check for report status updates (for real-time notifications)"""
    if request.method == 'GET':
        last_check = request.GET.get('last_check')
        
        # Get user's reports that have been updated since last check
        user_reports = Report.objects.filter(user=request.user)
        
        if last_check:
            from datetime import datetime
            try:
                last_check_dt = datetime.fromisoformat(last_check.replace('Z', '+00:00'))
                updated_reports = user_reports.filter(reviewed_at__gt=last_check_dt)
            except:
                updated_reports = user_reports.none()
        else:
            # First check - return recent activity
            updated_reports = user_reports.exclude(reviewed_at__isnull=True).order_by('-reviewed_at')[:3]
        
        updates = []
        for report in updated_reports:
            updates.append({
                'report_id': report.id,
                'status': report.workflow_status,
                'reviewed_by': report.reviewed_by.username if report.reviewed_by else None,
                'reviewed_at': report.reviewed_at.isoformat() if report.reviewed_at else None,
                'location': report.address[:50] if report.address else 'Unknown location'
            })
        
        return JsonResponse({
            'updates': updates,
            'has_updates': len(updates) > 0
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def edit_report(request, report_id):
    """Edit a pending report"""
    report = get_object_or_404(Report, id=report_id, user=request.user)
    
    # Only allow editing of pending reports
    if report.workflow_status != 'pending':
        messages.error(request, 'You can only edit reports that are still pending review.')
        return redirect('user_report_detail', report_id=report.id)
    
    if request.method == 'POST':
        from reports.forms import ReportForm
        form = ReportForm(request.POST, request.FILES, instance=report)
        
        if form.is_valid():
            updated_report = form.save(commit=False)
            updated_report.user = request.user  # Ensure user ownership
            updated_report.submitted_at = timezone.now()  # Update submission time
            updated_report.save()
            
            messages.success(request, f'Report #{report.id} has been updated successfully!')
            return redirect('user_report_detail', report_id=report.id)
    else:
        from reports.forms import ReportForm
        form = ReportForm(instance=report)
    
    return render(request, 'users/edit_report.html', {
        'form': form,
        'report': report,
    })


@login_required
def delete_report(request, report_id):
    """Delete a pending report"""
    report = get_object_or_404(Report, id=report_id, user=request.user)
    
    # Only allow deleting of pending reports
    if report.workflow_status != 'pending':
        messages.error(request, 'You can only delete reports that are still pending review.')
        return redirect('user_report_detail', report_id=report.id)
    
    if request.method == 'POST':
        report_id_deleted = report.id
        report.delete()
        messages.success(request, f'Report #{report_id_deleted} has been deleted successfully.')
        return redirect('dashboard')
    
    return render(request, 'users/confirm_delete.html', {
        'report': report,
    })

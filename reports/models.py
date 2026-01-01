from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import User  # Add this to link to logged-in users

class Report(models.Model):
    STATUS_CHOICES = (
        ('clean', 'Clean'),
        ('dirty', 'Dirty'),
    )
    
    WORKFLOW_STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('under_review', 'Under Review'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Allow null for anonymous users
    # photo = models.ImageField(upload_to='reports_photos/', blank=True, null=True)  # Optional photo
    photo = CloudinaryField('image', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    workflow_status = models.CharField(max_length=15, choices=WORKFLOW_STATUS_CHOICES, default='pending')
    location = models.CharField(max_length=255)
    review = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    location = models.CharField(max_length=255)
    address = models.CharField(max_length=500, blank=True, null=True)  # new field for human-readable address
    
    # Authority tracking fields
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_reports')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    authority_comments = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return f"{self.status.title()} report at {self.location}"


class Hotspot(models.Model):
    cluster_id = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    report_count = models.IntegerField()
    address = models.CharField(max_length=500, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Hotspot #{self.cluster_id} - {self.report_count} reports"

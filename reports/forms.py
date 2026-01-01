from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['photo', 'status', 'location', 'review']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 0.875rem 1rem; border: 2px solid var(--bg-secondary); border-radius: var(--border-radius); font-size: 1rem;'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12.9716,77.5946',
                'style': 'width: 100%; padding: 0.875rem 1rem; border: 2px solid var(--bg-secondary); border-radius: var(--border-radius); font-size: 1rem;'
            }),
            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the cleanliness issue in detail...',
                'style': 'width: 100%; padding: 0.875rem 1rem; border: 2px solid var(--bg-secondary); border-radius: var(--border-radius); font-size: 1rem; min-height: 120px; resize: vertical;'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'style': 'width: 100%; padding: 0.5rem; border: 2px dashed var(--bg-secondary); border-radius: var(--border-radius); background: var(--bg-secondary);'
            })
        }

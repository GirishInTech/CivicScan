from django.apps import AppConfig


class ReportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reports'
    
    def ready(self):
        pass # import reports.signals  # Disabled notification signals

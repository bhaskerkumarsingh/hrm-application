from django.db import models
from django.conf import settings

class DashboardPreference(models.Model):
    """Store user-specific dashboard preferences"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    layout = models.JSONField(default=dict)  # Store widget positions and sizes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dashboard preferences for {self.user}"
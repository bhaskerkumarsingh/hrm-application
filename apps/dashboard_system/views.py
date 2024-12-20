from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import DashboardService

class MainDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard_system/main.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dashboard_service = DashboardService()
        
        context.update({
            'attendance_summary': dashboard_service.get_attendance_summary(),
            'leave_statistics': dashboard_service.get_leave_statistics(),
            'recent_activities': dashboard_service.get_recent_activities(),
            'page_title': 'Dashboard',
        })
        return context
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Payroll
from .services import PayrollCalculator

class PayrollListView(LoginRequiredMixin, ListView):
    model = Payroll
    template_name = 'payroll_system/list.html'
    context_object_name = 'payroll_records'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Payroll.objects.all()
        return Payroll.objects.filter(employee=self.request.user)

class PayrollDetailView(LoginRequiredMixin, DetailView):
    model = Payroll
    template_name = 'payroll_system/detail.html'
    context_object_name = 'payroll'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breakdown'] = PayrollCalculator.get_salary_breakdown(self.object)
        return context
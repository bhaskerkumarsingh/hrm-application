from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReportGenerationForm
from .services import ReportGenerator

class AttendanceReportView(LoginRequiredMixin, FormView):
    template_name = 'reports/attendance.html'
    form_class = ReportGenerationForm
    success_url = '/reports/download/'
    
    def form_valid(self, form):
        report_generator = ReportGenerator()
        self.report_data = report_generator.generate_attendance_report(
            start_date=form.cleaned_data['start_date'],
            end_date=form.cleaned_data['end_date'],
            department=form.cleaned_data.get('department')
        )
        return super().form_valid(form)

class PayrollReportView(LoginRequiredMixin, FormView):
    template_name = 'reports/payroll.html'
    form_class = ReportGenerationForm
    success_url = '/reports/download/'
    
    def form_valid(self, form):
        report_generator = ReportGenerator()
        self.report_data = report_generator.generate_payroll_report(
            month=form.cleaned_data['month'],
            year=form.cleaned_data['year'],
            department=form.cleaned_data.get('department')
        )
        return super().form_valid(form)
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Attendance
from .forms import AttendanceForm

class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'attendance_management/list.html'
    context_object_name = 'attendance_records'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if date_filter := self.request.GET.get('date'):
            queryset = queryset.filter(date=date_filter)
        return queryset

class AttendanceMarkView(LoginRequiredMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'attendance_management/mark.html'
    success_url = '/attendance/'
    
    def form_valid(self, form):
        form.instance.marked_by = self.request.user
        return super().form_valid(form)
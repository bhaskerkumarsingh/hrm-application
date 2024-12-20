from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import LeaveRequest
from .forms import LeaveRequestForm

class LeaveRequestListView(LoginRequiredMixin, ListView):
    model = LeaveRequest
    template_name = 'leave_management/list.html'
    context_object_name = 'leave_requests'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return LeaveRequest.objects.all()
        return LeaveRequest.objects.filter(employee=self.request.user)

class LeaveRequestCreateView(LoginRequiredMixin, CreateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = 'leave_management/create.html'
    success_url = '/leave/'
    
    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Officer
from .forms import OfficerForm

class OfficerListView(LoginRequiredMixin, ListView):
    model = Officer
    template_name = 'officer_profiles/list.html'
    context_object_name = 'officers'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if search_query := self.request.GET.get('search'):
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

class OfficerDetailView(LoginRequiredMixin, DetailView):
    model = Officer
    template_name = 'officer_profiles/detail.html'
    context_object_name = 'officer'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attendance_history'] = self.object.get_attendance_history()
        context['leave_balance'] = self.object.get_leave_balance()
        return context
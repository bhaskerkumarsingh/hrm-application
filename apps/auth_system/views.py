from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm

class CustomLoginView(LoginView):
    template_name = 'auth_system/login.html'
    form_class = CustomAuthenticationForm
    
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'auth_system/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_roles'] = self.request.user.get_roles()
        return context
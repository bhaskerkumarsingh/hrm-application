from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if not request.path.startswith('/login/'):
                messages.warning(request, 'Please login to continue.')
                return redirect(reverse('login'))
        return self.get_response(request)
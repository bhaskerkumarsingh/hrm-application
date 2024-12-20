from django.db import connection
from django.http import Http404
from apps.saas.models import Tenant

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        hostname = request.get_host().split(':')[0]
        tenant = Tenant.objects.filter(domain=hostname).first()
        
        if not tenant:
            raise Http404("Tenant not found")
            
        connection.set_tenant(tenant)
        request.tenant = tenant
        
        return self.get_response(request)
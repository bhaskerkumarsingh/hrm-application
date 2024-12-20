"""
WSGI config for hrm_ai_system project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrm_ai_system.settings')

application = get_wsgi_application()
"""
ASGI config for PetRescue project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petrescue.settings')

application = get_asgi_application()

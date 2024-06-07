import os
import sys
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from channels.routing import get_default_application

application = get_asgi_application()
channel_layer = get_default_application()

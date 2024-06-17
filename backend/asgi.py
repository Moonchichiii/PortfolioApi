import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import livechat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Ensure Django is ready before initializing the ASGI application
django.setup()

from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            livechat.routing.websocket_urlpatterns
        )
    ),
})
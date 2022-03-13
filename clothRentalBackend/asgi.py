"""
ASGI config for clothRentalBackend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from notifications.channelsmiddleware import TokenAuthMiddleware
from clothRentalBackend.routing import websocket_urlpatterns 
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothRentalBackend.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    "websocket": TokenAuthMiddleware(
            URLRouter(websocket_urlpatterns)
        )
})

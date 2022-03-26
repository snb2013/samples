"""
ASGI config for myfirstbot project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import bot.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myfirstbot.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
            bot.routing.websocket_urlpatterns
        ),
    # Just HTTP for now. (We can add other protocols later.)
})

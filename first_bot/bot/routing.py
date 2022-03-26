from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('',  consumers.BotConsumer.as_asgi()),
]

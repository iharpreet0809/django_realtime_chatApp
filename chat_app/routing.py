from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Use integer for room ID to match the model
    re_path(r'ws/chat/(?P<room_name>\d+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/presence/$', consumers.PresenceConsumer.as_asgi()),
]
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat_app.routing
from chat_app.middleware import TokenAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_project.settings')
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(
        URLRouter(chat_app.routing.websocket_urlpatterns)
    ),
})
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

@database_sync_to_async
def get_user(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    """
    Custom middleware for token authentication in WebSocket connections
    """
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Parse query string for token
        query_string = scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)
        token_key = query_params.get('token', [None])[0]
        
        # Get user from token
        scope['user'] = await get_user(token_key) if token_key else AnonymousUser()
        
        return await self.inner(scope, receive, send) 
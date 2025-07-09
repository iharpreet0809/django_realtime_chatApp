from django.urls import path
from .views import (
    SignUpView, LoginView, ProfileView, 
    ChatRoomListView, MessageListView, StartChatView
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('start-chat/', StartChatView.as_view(), name='start-chat'), # New URL
    path('chats/', ChatRoomListView.as_view(), name='chat-list'),
    path('chats/<int:room_id>/messages/', MessageListView.as_view(), name='message-list'),
]
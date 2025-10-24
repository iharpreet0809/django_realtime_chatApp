from django.urls import path
from django.contrib.auth.views import LogoutView
from . import template_views as views

def chat_room(request, room_name):
    from django.shortcuts import render
    return render(request, 'chat_room.html', {
        'room_name': room_name
    })

urlpatterns = [
    # The root path '' now correctly points to the main chat home view.
    path('', views.chat_home, name='chat_home'),

    # The '/login/' path now correctly points to our custom login_view.
    path('login/', views.login_view, name='login'),
    path('login-success/', views.login_with_success_view, name='login_with_success'),

    # The '/logout/' path uses Django's built-in view for simplicity.
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # The '/register/' path points to our custom registration view.
    path('register/', views.register_view, name='register'),
    
    # Debug paths
    path('debug/', views.debug_view, name='debug'),
    path('quick-login/', views.quick_login_view, name='quick_login'),
    
    # Chat room path
    path('chat/<str:room_name>/', chat_room, name='chat_room'),
]


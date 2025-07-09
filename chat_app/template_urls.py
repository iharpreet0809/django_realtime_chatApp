from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView as AuthLoginView
from .forms import RegistrationForm # You'll need to create this form
from django.shortcuts import render, redirect
from .template_views import chat_home
from django.contrib.auth.views import LogoutView
from . import template_views as views

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def chat_room(request, room_name):
    return render(request, 'chat_room.html', {
        'room_name': room_name
    })

urlpatterns = [
    path('login/', AuthLoginView.as_view(template_name='login.html'), name='login'),
    path('register/', register, name='register'),
    path('chat/<str:room_name>/', chat_room, name='chat_room'),


    # The root path '' now correctly points to the main chat home view.
    path('', views.chat_home, name='chat_home'),

    # The '/login/' path now correctly points to our custom login_view.
    # path('login/', views.login_view, name='login'),

    # The '/logout/' path uses Django's built-in view for simplicity.
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # The '/register/' path points to our custom registration view.
    path('register/', views.register_view, name='register'),
]


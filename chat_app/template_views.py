from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from .models import ChatRoom

@login_required
def chat_home(request):
    """
    Displays the main chat interface for a logged-in user.
    """
    chat_rooms = request.user.chat_rooms.all()
    return render(request, 'chat_home.html', {'chat_rooms': chat_rooms})

def login_view(request):
    """
    Renders the login page. The actual login logic is handled by the
    frontend JavaScript making an API call.
    """
    return render(request, '/login.html')

def register_view(request):
    """
    Handles user registration. On successful registration, redirects to the login page.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            form.full_clean
            return redirect('login')
    else:
        form = RegistrationForm()
        form.full_clean
    return render(request, '/register.html', {'form': form})
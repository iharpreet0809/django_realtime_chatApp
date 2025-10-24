from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from .models import ChatRoom

def chat_home(request):
    """
    Displays the main chat interface for a logged-in user.
    """
    # If user is not authenticated via session, redirect to login
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get chat rooms with prefetched messages for better performance
    from django.db.models import Count, Q
    from chat_app.models import MessageStatus
    
    chat_rooms = request.user.chat_rooms.prefetch_related('messages', 'participants').all()
    
    # Calculate unread counts for each room
    for room in chat_rooms:
        # Count unread messages (messages where user hasn't seen them)
        unread_count = MessageStatus.objects.filter(
            message__room=room,
            user=request.user,
            status__in=['sent', 'delivered']  # Not 'seen'
        ).count()
        room.unread_count = unread_count
    
    return render(request, 'chat_home.html', {'chat_rooms': chat_rooms})

def debug_view(request):
    """Debug view to test user data"""
    if not request.user.is_authenticated:
        return redirect('quick_login')
    
    chat_rooms = request.user.chat_rooms.all()
    context = {
        'chat_rooms': chat_rooms,
        'debug_info': {
            'user_id': request.user.id,
            'username': request.user.username,
            'first_name': request.user.first_name,
            'email': request.user.email,
            'is_authenticated': request.user.is_authenticated,
            'room_count': chat_rooms.count(),
        }
    }
    return render(request, 'debug_template.html', context)

def quick_login_view(request):
    """Quick login for testing"""
    if request.user.is_authenticated:
        return redirect('chat_home')
    
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login
        from rest_framework.authtoken.models import Token
        
        identifier = request.POST.get('identifier')  # Changed from username
        password = request.POST.get('password')
        
        user = authenticate(request, identifier=identifier, password=password)
        if user is not None:
            login(request, user)
            # Also create/get API token for WebSocket authentication
            token, _ = Token.objects.get_or_create(user=user)
            
            # Pass token to template so it can be stored in localStorage
            context = {
                'user_token': token.key,
                'user_data': {
                    'username': user.username,
                    'first_name': user.first_name or user.username
                }
            }
            return render(request, 'login_success.html', context)
        else:
            return render(request, 'quick_login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'quick_login.html')

def login_view(request):
    """
    Renders the login page. The actual login logic is handled by the
    frontend JavaScript making an API call.
    """
    from .authentication import FlexibleAuthBackend
    
    if request.user.is_authenticated:
        return redirect('chat_home')
    
    # Handle form-based login as fallback
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login
        from rest_framework.authtoken.models import Token
        
        identifier = request.POST.get('identifier')  # Changed from username
        password = request.POST.get('password')
        
        user = authenticate(request, identifier=identifier, password=password)
        if user is not None:
            login(request, user)
            # Also create/get API token for WebSocket authentication
            token, _ = Token.objects.get_or_create(user=user)
            
            context = {
                'user_token': token.key,
                'user_data': {
                    'username': user.username,
                    'first_name': user.first_name or user.username
                }
            }
            return render(request, 'login_success.html', context)
        else:
            context = {
                'error': 'Invalid credentials',
                'login_placeholder': FlexibleAuthBackend.get_login_placeholder()
            }
            return render(request, 'chat_app/login.html', context)
    
    context = {
        'login_placeholder': FlexibleAuthBackend.get_login_placeholder()
    }
    return render(request, 'chat_app/login.html', context)

def register_view(request):
    """
    Handles user registration. On successful registration, redirects to the login page.
    """
    if request.user.is_authenticated:
        return redirect('chat_home')
        
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Redirect to login with success message
            return redirect('login_with_success')
    else:
        form = RegistrationForm()
    return render(request, 'chat_app/register.html', {'form': form})

def login_with_success_view(request):
    """Login page with registration success notification"""
    from .authentication import FlexibleAuthBackend
    
    if request.user.is_authenticated:
        return redirect('chat_home')
    
    # Handle form-based login as fallback
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login
        from rest_framework.authtoken.models import Token
        
        identifier = request.POST.get('identifier')  # Changed from username
        password = request.POST.get('password')
        
        user = authenticate(request, identifier=identifier, password=password)
        if user is not None:
            login(request, user)
            # Also create/get API token for WebSocket authentication
            token, _ = Token.objects.get_or_create(user=user)
            
            context = {
                'user_token': token.key,
                'user_data': {
                    'username': user.username,
                    'first_name': user.first_name or user.username
                }
            }
            return render(request, 'login_success.html', context)
        else:
            context = {
                'error': 'Invalid credentials', 
                'show_success': True,
                'login_placeholder': FlexibleAuthBackend.get_login_placeholder()
            }
            return render(request, 'chat_app/login.html', context)
    
    context = {
        'show_success': True,
        'login_placeholder': FlexibleAuthBackend.get_login_placeholder()
    }
    return render(request, 'chat_app/login.html', context)
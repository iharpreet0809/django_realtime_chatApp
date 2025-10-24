from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.db.models import Q

class FlexibleAuthBackend(BaseBackend):
    """
    Custom authentication backend that allows login with:
    - Username
    - Email 
    - Phone number
    
    Easily configurable by modifying the ALLOWED_LOGIN_FIELDS list
    """
    
    # Configuration: Add/remove fields as needed
    ALLOWED_LOGIN_FIELDS = [
        'username',     # Login with username
        'email',        # Login with email
        'phone_number', # Login with phone number (from profile)
    ]
    
    def authenticate(self, request, identifier=None, password=None, **kwargs):
        if identifier is None or password is None:
            return None
        
        # Build query based on allowed fields
        query = Q()
        
        if 'username' in self.ALLOWED_LOGIN_FIELDS:
            query |= Q(username=identifier)
            
        if 'email' in self.ALLOWED_LOGIN_FIELDS:
            query |= Q(email=identifier)
            
        if 'phone_number' in self.ALLOWED_LOGIN_FIELDS:
            query |= Q(profile__phone_number=identifier)
        
        try:
            user = User.objects.select_related('profile').get(query)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            # Handle edge case where multiple users match
            return None
        
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    @classmethod
    def get_login_placeholder(cls):
        """Generate placeholder text based on allowed fields"""
        field_names = []
        if 'username' in cls.ALLOWED_LOGIN_FIELDS:
            field_names.append('Username')
        if 'email' in cls.ALLOWED_LOGIN_FIELDS:
            field_names.append('Email')
        if 'phone_number' in cls.ALLOWED_LOGIN_FIELDS:
            field_names.append('Phone')
        
        if len(field_names) == 1:
            return field_names[0]
        elif len(field_names) == 2:
            return f"{field_names[0]} or {field_names[1]}"
        else:
            return f"{', '.join(field_names[:-1])} or {field_names[-1]}"
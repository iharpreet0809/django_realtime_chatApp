# Flexible Login Configuration Guide

## Overview
The login system supports multiple authentication methods through a single input field. Users can login with:
- Username
- Email address  
- Phone number

## Configuration

### Easy Configuration (chat_app/authentication.py)

To modify which login methods are allowed, simply edit the `ALLOWED_LOGIN_FIELDS` list in `FlexibleAuthBackend`:

```python
class FlexibleAuthBackend(BaseBackend):
    # Configuration: Add/remove fields as needed
    ALLOWED_LOGIN_FIELDS = [
        'username',     # Login with username
        'email',        # Login with email
        'phone_number', # Login with phone number (from profile)
    ]
```

### Common Configurations

#### 1. Username + Email Only (No Phone)
```python
ALLOWED_LOGIN_FIELDS = [
    'username',
    'email',
]
```
Result: Placeholder shows "Username or Email"

#### 2. Email Only
```python
ALLOWED_LOGIN_FIELDS = [
    'email',
]
```
Result: Placeholder shows "Email"

#### 3. Username Only (Traditional)
```python
ALLOWED_LOGIN_FIELDS = [
    'username',
]
```
Result: Placeholder shows "Username"

#### 4. Phone + Email Only
```python
ALLOWED_LOGIN_FIELDS = [
    'email',
    'phone_number',
]
```
Result: Placeholder shows "Email or Phone"

## How It Works

1. **User enters identifier** in single input field
2. **Backend checks** all allowed fields in database
3. **Matches user** if found in any allowed field
4. **Validates password** and logs in user
5. **Placeholder text** automatically updates based on configuration

## Files Modified

- `chat_app/authentication.py` - Main authentication logic
- `chat_project/settings.py` - Authentication backend configuration
- `chat_app/template_views.py` - View logic updates
- `chat_app/views.py` - API login updates
- `chat_app/templates/chat_app/login.html` - Frontend updates

## Benefits

- **Single input field** - Clean user experience
- **Flexible configuration** - Easy to modify in future
- **Backward compatible** - Supports old username-only systems
- **Dynamic placeholders** - UI updates automatically
- **Secure** - Uses Django's built-in authentication
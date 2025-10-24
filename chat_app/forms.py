from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    """
    A custom registration form with consistent styling and validation.
    """
    first_name = forms.CharField(
        label='First Name',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-700 bg-gray-900 placeholder-gray-500 focus:outline-none focus:ring-purple-500 focus:border-purple-500 focus:z-10 sm:text-sm rounded-t-md',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-700 bg-gray-900 placeholder-gray-500 focus:outline-none focus:ring-purple-500 focus:border-purple-500 focus:z-10 sm:text-sm',
            'placeholder': 'Last Name'
        })
    )
    username = forms.CharField(
        label='Username',
        min_length=4,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-700 bg-gray-900 placeholder-gray-500 focus:outline-none focus:ring-purple-500 focus:border-purple-500 focus:z-10 sm:text-sm',
            'placeholder': 'Username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-700 bg-gray-900 placeholder-gray-500 focus:outline-none focus:ring-purple-500 focus:border-purple-500 focus:z-10 sm:text-sm',
            'placeholder': 'Email address'
        })
    )
    phone_number = forms.CharField(
        label='Phone Number',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-700 bg-gray-900 placeholder-gray-500 focus:outline-none focus:ring-purple-500 focus:border-purple-500 focus:z-10 sm:text-sm',
            'placeholder': 'Phone Number (Optional)'
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-700 bg-gray-900 placeholder-gray-500 focus:outline-none focus:ring-purple-500 focus:border-purple-500 focus:z-10 sm:text-sm',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={
            'class': 'appearance-none rounded-none relative block w-full px-3 py-3 border border-gray-700 bg-gray-900 placeholder-gray-500 focus:outline-none focus:ring-purple-500 focus:border-purple-500 focus:z-10 sm:text-sm rounded-b-md',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Passwords don\'t match.')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
            
            # Force refresh to ensure signals have completed
            user.refresh_from_db()
            
            # Update profile with phone number if provided
            phone_number = self.cleaned_data.get('phone_number')
            if phone_number:
                from .models import Profile
                # Ensure profile exists (signals should have created it)
                profile, created = Profile.objects.get_or_create(user=user)
                profile.phone_number = phone_number
                profile.save()
        return user
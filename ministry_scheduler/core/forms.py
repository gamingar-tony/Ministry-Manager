from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Homily
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs = {'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs = {'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs = {'placeholder': 'Email'}),
        }

class HomilyForm(forms.ModelForm):
    class Meta:
        model = Homily
        fields = ['title', 'content', 'date', 'file']
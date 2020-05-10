from user.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.forms import TextInput,EmailInput,Select,FileInput

from django import forms


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username' : TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
            'email' : EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'first_name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'last_name'}),
        }
CITY = [
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Izmir', 'Izmir'),
    ('Mersin', 'Mersin'),
    ('Antalya', 'Antalya'),
    ('Adana', 'Adana'),
    ('Diyarbakir', 'Diyarbakir'),
]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'country', 'image')
        widgets = {
            'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'phone'}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'address'}),
            'city' : Select(attrs={'class': 'input', 'placeholder': 'city'},choices=CITY),
            'country': TextInput(attrs={'class': 'form-control', 'placeholder': 'country'}),
            'image' : FileInput(attrs={'class': 'input', 'placeholder': 'image'}),
        }
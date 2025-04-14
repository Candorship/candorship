from django import forms
from django.contrib.auth import authenticate

from .models import User


class SignupForm(forms.Form):
    email = forms.EmailField(
        required=True,
    )
    password = forms.CharField(
        required=True,
    )
    password2 = forms.CharField(
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            self.add_error('password2', "Passwords don't match.")

        email = cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            self.add_error('email', 'Email is used by an existing account.')

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username'}
        ),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                self.add_error(
                    'username', 'Invalid username or password. Please try again.'
                )
            else:
                # Add the authenticated user to cleaned_data
                cleaned_data['user'] = user

        return cleaned_data

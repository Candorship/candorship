from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    remember_me = forms.BooleanField(required=False)

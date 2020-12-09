from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# A form to register a user
class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

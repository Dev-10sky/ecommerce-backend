from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django import forms
from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("first_name", "last_name", "email")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email")

class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')
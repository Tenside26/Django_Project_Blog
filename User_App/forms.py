from django.contrib.admin.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUserModel


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=40, label="Username")
    password = forms.CharField(max_length=40, label="Password", widget=forms.PasswordInput)


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUserModel
        fields = ["username", "first_name", "last_name", "email"]


class UserUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = CustomUserModel
        fields = ["username", "first_name", "last_name", "email", "info", "age", "picture"]


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Repeat New Password")

    class Meta:
        model = CustomUserModel
        fields = ["old_password", "new_password1", "new_password2"]

import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "auth-input",
                "autocomplete": "off",
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "auth-input",
                "autocomplete": "new-password",
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm Password", "class": "auth-input"}
        )
    )

    class Meta:
        model = User
        fields = ["username", "password"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not re.match(r"^[A-Za-z0-9_-]{3,20}$", username):
            raise forms.ValidationError(
                "3–20 characters. Letters, numbers, underscores and hyphens only."
            )
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("That username is already taken.")
        return username

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get("password")
        cpw = cleaned.get("confirm_password")
        if pw and cpw and pw != cpw:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "auth-input",
                "autocomplete": "username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "auth-input",
                "autocomplete": "current-password",
            }
        )
    )

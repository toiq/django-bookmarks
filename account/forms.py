from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    repeat_password = forms.CharField(
        widget=forms.PasswordInput, label="Repeat Password"
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "email"]

    def clean_reset_password(self):
        cd = self.cleaned_data
        if cd["password"] != cd["repeat_password"]:
            raise forms.ValidationError("Passwords don't match.")
        return cd["repeat_password"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Email already exists")

        return data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        data = self.cleaned_data["email"]

        if User.objects.filter(email=data).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError("Email already exists")
        return data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["date_of_birth", "photo"]

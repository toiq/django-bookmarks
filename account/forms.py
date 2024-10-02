from django import forms
from django.contrib.auth import get_user_model

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


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["date_of_birth", "photo"]

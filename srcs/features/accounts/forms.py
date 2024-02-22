from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from features.accounts.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["picture"]


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    picture = forms.ImageField()

    class Meta:
        model = User
        fields = ["picture", "username", "email", "password1", "password2"]

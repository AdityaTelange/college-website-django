from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (UserCreationForm as DjangoUserCreationForm)
from django.contrib.auth.forms import UsernameField

from . import models


class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = models.User
        fields = ("email",)
        field_classes = {"email": UsernameField}


class AuthenticationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(strip=False, widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get("username")

        password = self.cleaned_data.get("password")
        if username is not None and password:
            self.user = authenticate(self.request, username=username, password=password)
        if self.user is None:
            raise forms.ValidationError("Invalid username/password combination.")
        return self.cleaned_data

    def get_user(self):
        return self.user

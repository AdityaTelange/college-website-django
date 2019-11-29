from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (UserCreationForm as DjangoUserCreationForm)
from django.contrib.auth.forms import UsernameField
from django.core.mail import send_mail

from . import models


class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = models.User
        fields = ("email",)
        field_classes = {"email": UsernameField}

    def send_mail(self):
        logger.info("Sending signup email for email=%s", self.cleaned_data["email"], )
        message = "Welcome {}".format(self.cleaned_data["email"])
        send_mail("Welcome to BookTime", message, "site@booktime.domain", [self.cleaned_data["email"]],
                  fail_silently=True, )


class AuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(strip=False, widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")

        password = self.cleaned_data.get("password")
        if email is not None and password:
            self.user = authenticate(self.request, email=email, password=password)
        if self.user is None:
            raise forms.ValidationError("Invalid email/password combination.")
        return self.cleaned_data

    def get_user(self):
        return self.user

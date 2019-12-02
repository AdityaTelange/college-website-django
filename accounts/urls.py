"""webpage URL Configuration
"""
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import RedirectView

from . import forms
from . import views

urlpatterns = [
    path("", RedirectView.as_view(url='login', permanent=True, )),
    path("login/",
         auth_views.LoginView.as_view(template_name="login.html",
                                      form_class=forms.AuthenticationForm,
                                      redirect_authenticated_user=True),
         name="login",
         kwargs={'redirect_authenticated_user': True}),
    path("logout/",
         auth_views.LogoutView.as_view(),
         name="logout"),
    path("profile/",
         views.ProfileView.as_view(),
         name="profile", ),
]

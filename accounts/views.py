from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from django.views.generic.edit import (
    FormView,
)
from django.views.generic.list import ListView

from . import forms
from . import models


class SignupView(FormView):
    template_name = "signup.html"
    form_class = forms.UserCreationForm

    success_url = "/"

    def get_success_url(self):
        redirect_to = self.request.GET.get("next", "/")
        return redirect_to

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")
        user = authenticate(email=email, password=raw_password)
        login(self.request, user)
        form.send_mail()
        messages.info(self.request, "You signed up successfully.")
        return response


def logout_view(request):
    logout(request)


class ProfileView(LoginRequiredMixin, ListView):
    template_name = "profile.html"
    model = models.User

    def get_queryset(self):
        print(self.request.user)
        return self.model.objects.filter(email=self.request.user)

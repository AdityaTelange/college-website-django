from django.contrib.auth import logout
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from django.views.generic.list import ListView

from . import models


def logout_view(request):
    logout(request)


class ProfileView(LoginRequiredMixin, ListView):
    template_name = "profile.html"
    model = models.User

    def get_queryset(self):
        return self.model.objects.filter(email=self.request.user)

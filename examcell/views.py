from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from django.views.generic.dates import (
    ArchiveIndexView)
from django.views.generic.list import ListView

from .models import Result


class ExamCellIndex(LoginRequiredMixin, ListView):
    template_name = "examcell_index.html"

    def get_queryset(self):
        pass


class ExamCellResults(LoginRequiredMixin, ArchiveIndexView):
    date_field = 'pub_date'
    template_name = "results/examcell_results.html"
    allow_empty = True

    def get_queryset(self):
        return Result.objects.published()

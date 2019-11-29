from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from django.views.generic.dates import (
    ArchiveIndexView, )
from django.views.generic.list import ListView

from .models import Result


class ResultViewMixin:
    date_field = 'pub_date'
    paginate_by = 10

    def __init__(self):
        self.request = None

    def get_allow_future(self):
        return self.request.user.is_staff

    def get_queryset(self):
        if self.request.user.is_staff:
            return Result.objects.all()
        else:
            return Result.objects.published()


class ExamCellIndex(LoginRequiredMixin, ListView):
    template_name = "examcell_index.html"

    def get_queryset(self):
        pass


class ExamCellResults(LoginRequiredMixin, ResultViewMixin, ArchiveIndexView):
    template_name = "results/examcell_results.html"

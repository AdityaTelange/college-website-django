from django.contrib import admin

from .models import Result


# admin.site.register(Result)


class ResultAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("type", "year", "branch", "pattern_yr", "semester", "pattern", "exam_month", "exam_year")}
    search_fields = ("type", "year", "branch", "pattern_yr", "semester", "pattern", "exam_month", "exam_year")

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return list(self.readonly_fields) + ["slug", "branch"]

    def get_prepopulated_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.prepopulated_fields
        else:
            return {}


admin.site.register(Result, ResultAdmin)

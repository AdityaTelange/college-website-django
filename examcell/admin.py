from django.contrib import admin

from .models import (
    Result, ResultTypeTag, ResultBranchTag, ResultPatternYrTag, ResultPatternTag, ResultSemesterTag, ResultExamMonthTag,
    ResultYearTag
)


class ResultAdmin(admin.ModelAdmin):
    # ref:https://stackoverflow.com/a/36940373
    search_fields = (
        "type__name", "year__name", "branch__name", "pattern_year__name", "semester__name", "pattern__name",
        "exam_month__name", "exam_year"
    )
    list_filter = ('type', 'year', 'branch')
    list_display = (
        ['type', 'year', 'branch', 'pattern_year', 'semester', 'pattern', 'exam_month', 'exam_year', 'is_active'])

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return list(self.readonly_fields) + ["author", "pub_date"]

    actions = ["mark_active", "mark_inactive"]

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)


class TypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return list(self.readonly_fields) + ["name"]

    def get_prepopulated_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.prepopulated_fields
        else:
            return {}


admin.site.register(Result, ResultAdmin)
admin.site.register(ResultTypeTag, TypeAdmin)
admin.site.register(ResultBranchTag, TypeAdmin)
admin.site.register(ResultPatternYrTag, TypeAdmin)
admin.site.register(ResultPatternTag, TypeAdmin)
admin.site.register(ResultSemesterTag, TypeAdmin)
admin.site.register(ResultExamMonthTag, TypeAdmin)
admin.site.register(ResultYearTag, TypeAdmin)

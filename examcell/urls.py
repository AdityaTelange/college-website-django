"""webpage URL Configuration
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.ExamCellIndex.as_view(), name='examcell'),
    path('results/', views.ExamCellResults.as_view(), name='examcell_results'),
]

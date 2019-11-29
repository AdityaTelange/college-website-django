"""webpage URL Configuration
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='root'),
    path('about-us/', views.AboutUs.as_view(), name='about_us'),
    path('contact-us/', views.ContactUS.as_view(), name='contact_us'),
]

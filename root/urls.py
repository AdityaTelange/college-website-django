"""webpage URL Configuration
"""
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from . import views
from .sitemap import ViewSitemap

urlpatterns = [
    path('', views.Index.as_view(), name='root'),
    path('about-us/', views.AboutUs.as_view(), name='about_us'),
    path('contact-us/', views.ContactUS.as_view(), name='contact_us'),
    path('sitemap.xml', sitemap, {'sitemaps': {'static': ViewSitemap}}),
]

"""webpage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('root.urls'), name='root'),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('examcell/', include('examcell.urls'), name='examcell')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

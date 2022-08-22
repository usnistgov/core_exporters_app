""" Conf urls
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import re_path

from core_exporters_app import urls as core_exporters_app_urls

urlpatterns = [
    re_path(r"^admin/", include(admin.site.urls)),
] + core_exporters_app_urls.urlpatterns

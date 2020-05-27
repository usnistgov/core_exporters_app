""" Url router for the exporters application
"""
from django.conf.urls import include
from django.urls import re_path

from core_exporters_app.views.user import ajax as user_ajax, views as user_views

urlpatterns = [
    re_path(r"^rest/", include("core_exporters_app.rest.urls")),
    re_path(
        r"^selection",
        user_ajax.exporters_selection,
        name="core_exporters_app_exporters_selection",
    ),
    re_path(
        r"^open-form",
        user_ajax.open_form,
        name="core_exporters_app_exporters_open_form",
    ),
    re_path(
        r"^download",
        user_views.download_exported_compressed_file,
        name="core_exporters_app_exporters_download",
    ),
    re_path(
        r"^status-file",
        user_ajax.check_download_status,
        name="core_exporters_app_exporters_check_download",
    ),
    re_path(r"^", include("core_exporters_app.exporters.urls")),
]

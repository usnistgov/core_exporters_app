""" Exporters urls
"""
from django.conf.urls import include
from django.urls import re_path

urlpatterns = [
    re_path("", include("core_exporters_app.exporters.json_exporter.urls")),
    re_path("", include("core_exporters_app.exporters.xml.urls")),
    re_path("", include("core_exporters_app.exporters.blob.urls")),
]

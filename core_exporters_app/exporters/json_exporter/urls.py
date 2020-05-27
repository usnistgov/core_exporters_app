""" Json exporter url
"""

from django.urls import re_path

from core_exporters_app.exporters.json_exporter.models import JsonExporter

urlpatterns = [
    re_path("", JsonExporter, {"name": "JSON", "enable_by_default": True}),
]

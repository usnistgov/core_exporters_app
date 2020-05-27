""" Json exporter url
"""

from django.urls import re_path

from core_exporters_app.exporters.blob.models import BlobExporter

urlpatterns = [
    re_path("", BlobExporter, {"name": "BLOB", "enable_by_default": True}),
]

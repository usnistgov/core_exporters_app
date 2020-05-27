""" Xml exporter url
"""

from django.urls import re_path

from core_exporters_app.exporters.xml.models import XmlExporter

urlpatterns = [
    re_path("", XmlExporter, {"name": "XML", "enable_by_default": True}),
]

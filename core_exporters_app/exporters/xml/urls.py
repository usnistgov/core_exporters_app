""" Xml exporter url
"""
from django.conf.urls import url

from models import XmlExporter

urlpatterns = [
   url('', XmlExporter, {'name': 'XML', 'enable_by_default': True}),
]

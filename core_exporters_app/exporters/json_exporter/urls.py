""" Json exporter url
"""
from django.conf.urls import url

from models import JsonExporter

urlpatterns = [
   url('', JsonExporter, {'name': 'JSON', 'enable_by_default': True}),
]

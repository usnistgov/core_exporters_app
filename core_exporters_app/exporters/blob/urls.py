""" Json exporter url
"""
from django.conf.urls import url

from models import BlobExporter

urlpatterns = [
   url('', BlobExporter, {'name': 'BLOB', 'enable_by_default': True}),
]

""" Json exporter url
"""
from django.conf.urls import patterns, url


urlpatterns = patterns(
   '',
   url('', 'core_exporters_app.exporters.blob.models.BlobExporter', {'name': 'BLOB', 'enable_by_default': True}),
)

""" Json exporter url
"""
from django.conf.urls import patterns, url


urlpatterns = patterns(
   '',
   url('', 'core_exporters_app.exporters.json.models.JsonExporter', {'name': 'JSON', 'enable_by_default': True}),
)

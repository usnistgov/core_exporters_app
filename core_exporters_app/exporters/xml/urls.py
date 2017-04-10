""" Xml exporter url
"""
from django.conf.urls import patterns, url


urlpatterns = patterns(
   '',
   url('', 'core_exporters_app.exporters.xml.models.XmlExporter', {'name': 'XML', 'enable_by_default': True}),
)

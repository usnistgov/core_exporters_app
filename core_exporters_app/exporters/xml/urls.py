""" Xml exporter url
"""
from django.conf.urls import patterns, url
from core_exporters_app.commons.constants import XML_URL


urlpatterns = patterns(
   '',
   url('', XML_URL, {'name': 'XML', 'enable_by_default': True}),
)

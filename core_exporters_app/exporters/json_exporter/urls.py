""" Json exporter url
"""
from django.conf.urls import patterns, url
from core_exporters_app.commons.constants import JSON_URL


urlpatterns = patterns(
   '',
   url('', JSON_URL, {'name': 'JSON', 'enable_by_default': True}),
)

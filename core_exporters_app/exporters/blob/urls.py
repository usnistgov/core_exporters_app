""" Json exporter url
"""
from django.conf.urls import patterns, url
from core_exporters_app.commons.constants import BLOB_URL


urlpatterns = patterns(
   '',
   url('', BLOB_URL, {'name': 'BLOB', 'enable_by_default': True}),
)

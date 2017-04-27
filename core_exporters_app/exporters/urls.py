""" Exporters urls
"""
from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    url('', include('core_exporters_app.exporters.json.urls')),
    url('', include('core_exporters_app.exporters.xml.urls')),
    url('', include('core_exporters_app.exporters.blob.urls')),
)


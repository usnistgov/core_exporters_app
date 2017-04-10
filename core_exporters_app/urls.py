""" Url router for the exporters application
"""
from django.conf.urls import url, include


urlpatterns = [
    url(r'^', include('core_exporters_app.exporters.urls')),
]

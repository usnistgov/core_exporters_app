""" Url router for the REST API
"""
from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from core_exporters_app.rest.export.data import views as export_data_views
from core_exporters_app.rest.exporters import views as exporters_views
from core_exporters_app.rest.exporters.xsl import views as xsl_views

urlpatterns = [
    re_path(
        r"^exporter/export/$",
        exporters_views.ExportToZip.as_view(),
        name="core_exporters_app_rest_exporter_export",
    ),
    re_path(
        r"^exporter/xsl/$",
        xsl_views.ExporterXslList.as_view(),
        name="core_exporters_app_rest_exporter_xsl",
    ),
    re_path(
        r"^exporter/xsl/(?P<pk>\w+)/$",
        xsl_views.ExporterXslDetail.as_view(),
        name="core_exporters_app_rest_exporter_xsl_detail",
    ),
    re_path(
        r"^exporter/$",
        exporters_views.ExporterList.as_view(),
        name="core_exporters_app_rest_exporter",
    ),
    re_path(
        r"^exporter/(?P<pk>\w+)/$",
        exporters_views.ExporterDetail.as_view(),
        name="core_exporters_app_rest_exporter_detail",
    ),
    re_path(
        r"^exporter/export/download/(?P<pk>\w+)/$",
        exporters_views.ExporterDownload.as_view(),
        name="core_exporters_app_rest_exporter_export_download",
    ),
    re_path(
        r"^export$",
        export_data_views.ExportData.as_view(),
        name="core_exporters_app_rest_export_data",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)

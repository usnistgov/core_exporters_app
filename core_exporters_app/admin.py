"""
Url router for the administration site
"""
from django.conf.urls import include
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import re_path

from core_main_app.admin import core_admin_site

from core_exporters_app.components.exported_compressed_file.admin_site import (
    CustomExportedCompressedFileAdmin,
)
from core_exporters_app.components.exported_compressed_file.models import (
    ExportedCompressedFile,
)
from core_exporters_app.components.exporter.admin_site import (
    CustomExporterAdmin,
)
from core_exporters_app.components.exporter.models import Exporter
from core_exporters_app.views.admin import (
    views as admin_views,
    ajax as admin_ajax,
)


admin_urls = [
    re_path(
        r"^exporters/(?P<pk>[\w-]+)/edit/$",
        staff_member_required(admin_ajax.EditExporterView.as_view()),
        name="core_exporters_app_exporters_edit",
    ),
    re_path(
        r"^exporters/xsl/(?P<pk>[\w-]+)/edit/$",
        staff_member_required(admin_ajax.EditExporterXslView.as_view()),
        name="core_exporters_app_exporters_xsl_edit",
    ),
    re_path(
        r"^exporters/associated-templates",
        staff_member_required(admin_ajax.associated_templates),
        name="core_exporters_app_exporters_associated_templates",
    ),
    re_path(
        r"^exporters",
        admin_views.manage_exporters,
        name="core_exporters_app_exporters",
    ),
    re_path(r"^xsl", include("core_exporters_app.exporters.xsl.urls")),
]

admin.site.register(Exporter, CustomExporterAdmin)
admin.site.register(ExportedCompressedFile, CustomExportedCompressedFileAdmin)

urls = core_admin_site.get_urls()
core_admin_site.get_urls = lambda: admin_urls + urls

"""
Url router for the administration site
"""
from django.conf.urls import include
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import re_path

from core_exporters_app.views.admin import views as admin_views, ajax as admin_ajax

admin_urls = [
    re_path(
        r"^exporters/(?P<pk>[\w-]+)/edit/$",
        staff_member_required(admin_ajax.EditExporterView.as_view()),
        name="core_exporters_app_exporters_edit",
    ),
    re_path(
        r"^exporters/associated-templates",
        staff_member_required(admin_ajax.associated_templates),
        name="core_exporters_app_exporters_associated_templates",
    ),
    re_path(
        r"^exporters", admin_views.manage_exporters, name="core_exporters_app_exporters"
    ),
    re_path(r"^xsl", include("core_exporters_app.exporters.xsl.urls")),
]

urls = admin.site.get_urls()
admin.site.get_urls = lambda: admin_urls + urls

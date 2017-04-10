"""
Url router for the administration site
"""
from django.contrib import admin
from django.conf.urls import url

from views.admin import views as admin_views, ajax as admin_ajax

admin_urls = [
    url(r'^exporters/edit', admin_ajax.edit_exporter,
        name='core_exporters_app_exporters_edit'),
    url(r'^exporters/associated-templates', admin_ajax.associated_templates,
        name='core_exporters_app_exporters_associated_templates'),
    url(r'^exporters', admin_views.manage_exporters,
        name='core_exporters_app_exporters'),
]

urls = admin.site.get_urls()
admin.site.get_urls = lambda: admin_urls + urls

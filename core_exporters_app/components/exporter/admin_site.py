""" Custom admin site for the Exporter model
"""
from django.contrib import admin


class CustomExporterAdmin(admin.ModelAdmin):
    """CustomExporterAdmin"""

    exclude = ["_cls", "url"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Exporters"""
        return False

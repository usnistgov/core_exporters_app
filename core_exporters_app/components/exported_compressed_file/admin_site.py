""" Custom admin site for the Exported Compressed File model
"""
from django.contrib import admin


class CustomExportedCompressedFileAdmin(admin.ModelAdmin):
    """CustomExportedCompressedFileAdmin"""

    readonly_fields = ["file_name", "file", "mime_type"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Exported Compressed File"""
        return False

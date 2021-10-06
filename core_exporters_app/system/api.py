""" System API for Exported files.
"""
from datetime import timedelta

from django.utils import timezone

from core_exporters_app.components.exported_compressed_file.models import (
    ExportedCompressedFile,
)


def get_older_exported_files(seconds):
    """Get older exported files

    Returns:

    """
    exported_files = [
        exported_file
        for exported_file in ExportedCompressedFile.objects.all()
        if exported_file.creation_date < timezone.now() - timedelta(seconds=seconds)
    ]
    return exported_files

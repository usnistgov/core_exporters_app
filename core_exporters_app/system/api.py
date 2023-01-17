""" System API for Exported files.
"""

from core_exporters_app.components.exported_compressed_file.models import (
    ExportedCompressedFile,
)
from core_main_app.utils.datetime import datetime_now, datetime_timedelta


def get_older_exported_files(seconds):
    """Get older exported files

    Returns:

    """
    exported_files = [
        exported_file
        for exported_file in ExportedCompressedFile.objects.all()
        if exported_file.creation_date
        < datetime_now() - datetime_timedelta(seconds=seconds)
    ]
    return exported_files

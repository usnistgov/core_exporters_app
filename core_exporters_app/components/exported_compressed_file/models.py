""" Exported Compressed File model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions
from core_main_app.utils.storage.storage import core_file_storage
from core_exporters_app.settings import EXPORTED_COMPRESSED_FILE_FOLDER


class ExportedCompressedFile(models.Model):
    """Represents exported files"""

    file_name = models.CharField(blank=False, max_length=200)
    file = models.FileField(
        blank=True,
        null=True,
        upload_to=EXPORTED_COMPRESSED_FILE_FOLDER,
        storage=core_file_storage(model="exported_compressed_files"),
    )
    is_ready = models.BooleanField(default=False)
    mime_type = models.CharField(blank=False, max_length=200)
    user_id = models.CharField(
        blank=False, max_length=200
    )  # FIXME: point to User
    creation_date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_by_id(object_id):
        """Get Exported compressed file with the given id

        Args:
            object_id:

        Returns:

        """
        try:
            return ExportedCompressedFile.objects.get(pk=str(object_id))
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

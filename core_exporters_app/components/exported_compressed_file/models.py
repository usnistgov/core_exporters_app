""" Exported Compressed File model
"""

from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors

from core_exporters_app.settings import GRIDFS_EXPORTED_COMPRESSED_FILE_COLLECTION
from core_main_app.commons import exceptions


class ExportedCompressedFile(Document):
    """Represents exported files"""

    file_name = fields.StringField()
    file = fields.FileField(
        blank=True, collection_name=GRIDFS_EXPORTED_COMPRESSED_FILE_COLLECTION
    )
    is_ready = fields.BooleanField(default=False)
    mime_type = fields.StringField()
    user_id = fields.StringField(blank=False)

    @staticmethod
    def get_by_id(object_id):
        """Get Exported compressed file with the given id

        Args:
            object_id:

        Returns:

        """
        try:
            return ExportedCompressedFile.objects.get(pk=str(object_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

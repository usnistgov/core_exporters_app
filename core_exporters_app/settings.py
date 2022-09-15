""" Core exporters app settings.

Settings with the following syntax can be overwritten at the project level:
SETTING_NAME = getattr(settings, "SETTING_NAME", "Default Value")
"""
from django.conf import settings

if not settings.configured:
    settings.configure()

# GridFS
EXPORTED_COMPRESSED_FILE_FOLDER = getattr(
    settings,
    "EXPORTED_COMPRESSED_FILE_FOLDER",
    "exporter_compressed_files",
)

COMPRESSED_FILES_EXPIRE_AFTER_SECONDS = getattr(
    settings,
    "COMPRESSED_FILES_EXPIRE_AFTER_SECONDS",
    3600,
)

CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = getattr(
    settings, "CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT", False
)
""" :py:class:`bool`: Can anonymous user access public document.
"""

MAX_DOCUMENT_LIST = getattr(settings, "MAX_DOCUMENT_LIST", 100)
""" :py:class:`int`: Maximum number of documents to be returned at once by the api.
"""

""" Exporter User views
"""
import logging

from django.http.response import HttpResponse

from core_main_app.commons import exceptions
from core_main_app.utils.rendering import render
import core_exporters_app.components.exported_compressed_file.api as exported_file_api

logger = logging.getLogger(__name__)


def download_exported_compressed_file(request):
    """Download view, ID file expected in parameters

    Args:
        request:

    Returns:

    """
    exporter_file_id = request.GET["id"]
    exported_file = None

    # Generate a default context
    context = {
        "message": "Please wait, the download will start automatically",
        "is_ready": False,
        "id_file": exporter_file_id,
    }

    try:
        # Get the exported file with the given id
        exported_file = exported_file_api.get_by_id(
            exporter_file_id, request.user
        )
    except exceptions.DoesNotExist:
        context["message"] = "The file with the given id does not exist."
    except Exception as exception:
        logger.error(
            "Something went wrong while downloading: %s", str(exception)
        )
        context[
            "message"
        ] = "Something went wrong while downloading. Please contact administrator"

    if exported_file and exported_file.is_ready:
        # the file is ready to be downloaded
        response = HttpResponse(exported_file.file.read())
        response["Content-Disposition"] = (
            "attachment; filename=" + exported_file.file_name
        )
        response["Content-Type"] = exported_file.mime_type
        return response

    # Add assets
    assets = {
        "js": [
            {
                "path": "core_exporters_app/user/js/exporter_compressed_file/download.js",
                "is_raw": False,
            }
        ],
        "css": [],
    }

    # Set page title
    context.update({"page_title": "Download Exported Files"})

    # Render the page
    return render(
        request,
        "core_exporters_app/user/exported_compressed_file/download.html",
        context=context,
        assets=assets,
    )

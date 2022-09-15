""" REST Views for Data Exporting
"""

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.commons import exceptions
from core_main_app.utils.file import get_file_http_response
import core_main_app.components.data.api as data_api
from core_explore_common_app.components.result.models import Result

import core_exporters_app.commons.constants as exporter_constants
import core_exporters_app.components.exported_compressed_file.api as exported_compressed_file_api
import core_exporters_app.components.exporter.api as exporter_api
from core_exporters_app.components.exported_compressed_file.models import (
    ExportedCompressedFile,
)
import core_exporters_app.exporters.xsl.api as exporter_xsl_api
from core_exporters_app.exporters.exporter import (
    get_exporter_module_from_url,
    AbstractExporter,
)
from core_exporters_app.rest.exporters.serializers import (
    ExporterExportedCompressedFileSerializer,
)


class ExportData(APIView):
    """Export Data"""

    def get(self, request):
        """Get the transformed Data file

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: transformed data
            - code: 400
              content: Validation error
            - code: 404
              content: Object not found error
            - code: 500
              content: Internal server error
        """
        try:
            document = "Data"
            # get data by id/pid
            if "data_id" in request.GET:
                data = data_api.get_by_id(request.GET["data_id"], request.user)
            # Check if 'core_linked_records_app' is installed before using pid
            elif "data_pid" in request.GET:
                if "core_linked_records_app" in settings.INSTALLED_APPS:
                    from core_linked_records_app.components.data import (
                        api as linked_data_api,
                    )

                    data = linked_data_api.get_data_by_pid(
                        request.GET["data_pid"], request
                    )
                else:
                    content = {"message": "module 'core_linked_records_app' not found."}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

            else:
                content = {"message": "data id/pid is missing or the value is empty."}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            if "exporter" not in request.GET:
                content = {"message": "exporter is missing or the value is empty."}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            document = "Exporter"
            # get the exporter with the given name
            exporter_object = exporter_api.get_by_name(request.GET["exporter"])

            # check if template is linked to the exporter
            if not exporter_object.has_template(data.template):
                content = {"message": "template not linked to this exporter"}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            # get the exporter module
            exporter_module = get_exporter_module_from_url(exporter_object.url)

            # if is a xslt transformation, we have to set the xslt
            if exporter_object.url == exporter_constants.XSL_URL:
                # get the exporter xsl object instead of exporter
                exporter_object = exporter_xsl_api.get_by_name(request.GET["exporter"])
                # set the xslt
                exporter_module.set_xslt(exporter_object.xsl_transformation)

            # get the list of the transformed result
            transform_result_list = exporter_module.transform(
                [Result(title=data.title, xml_content=data.xml_content)],
                request.session.session_key,
            )

            # Check if the list is empty
            if transform_result_list:
                return export_data(transform_result_list, request.user, data.title)

            content = {"message": "error during the transformation"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        except exceptions.DoesNotExist:
            content = {"message": document + " not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def export_data(transform_result_list, user, title):
    """Get the transformed Data file

    Args:
        transform_result_list:
        user:
        title:

    Returns:
        HttpResponse:
    """
    # get the list of the transformed content(first element since we have only one data)
    transform_result_content_list = transform_result_list[0].transform_result_content

    file_content = ""
    file_name = title
    extension = ""
    content_type = ""
    if len(transform_result_content_list) > 1:
        # export as a zip file (more than file)
        exported_file = ExportedCompressedFile(
            file_name="Query_Results.zip",
            is_ready=False,
            mime_type="application/zip",
            user_id=str(user.id),
        )

        # Save in database to generate an Id and be accessible via url
        exported_compressed_file_api.upsert(exported_file)

        # Export in Zip
        AbstractExporter.export(exported_file.id, transform_result_list, user)

        # Serialize object
        return_value = ExporterExportedCompressedFileSerializer(exported_file)
        compressed_file_object = exported_compressed_file_api.get_by_id(
            return_value.data["id"], user
        )

        file_content = compressed_file_object.file.read()
        file_name = compressed_file_object.file_name

    elif len(transform_result_content_list) == 1:
        # export as a ordinary file (first element since we have only one transformed content)
        file_content = transform_result_content_list[0].content_converted

        # get the extension
        extension = transform_result_content_list[0].content_extension

        # get the type content by removing '.' from the extension
        if extension:
            content_type = "text/" + extension.split(".")[1]

    return get_file_http_response(
        file_content,
        file_name,
        content_type,
        extension,
    )

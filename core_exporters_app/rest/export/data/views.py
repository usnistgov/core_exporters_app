""" REST Views for Data Exporting
"""

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http.response import HttpResponseBadRequest
import core_exporters_app.commons.constants as exporter_constants
import core_exporters_app.components.exporter.api as exporter_api
import core_main_app.components.data.api as data_api
from core_explore_common_app.components.result.models import Result
from core_exporters_app.exporters.exporter import (
    get_exporter_module_from_url,
)
from django.conf import settings
from core_main_app.utils.file import get_file_http_response
from core_main_app.commons import exceptions


class ExportData(APIView):
    """Export Data"""

    permission_classes = (IsAuthenticated,)

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

            document = "Exporter"
            # get the exporter with the given name
            exporter_object = exporter_api.get_by_name(request.GET["exporter"])

            # get the exporter module
            exporter_module = get_exporter_module_from_url(exporter_object.url)

            # if is a xslt transformation, we have to set the xslt
            if exporter_object.url == exporter_constants.XSL_URL:
                # set the xslt
                exporter_module.set_xslt(exporter_object.xsl_transformation)

            # get the list of the transformed result
            transform_result_list = exporter_module.transform(
                [Result(title=data.title, xml_content=data.xml_content)],
                request.session.session_key,
            )

            # Check if the list is empty
            if transform_result_list:
                # get the list of the transformed content(first element since we have only one data)
                transform_result_content_list = transform_result_list[
                    0
                ].transform_result_content

                content_type = ""
                extension = ""
                content_converted = ""

                # Check if the content is empty
                if transform_result_content_list:
                    # get the content  (first element since we have only one transformed content)
                    transform_result_content = transform_result_content_list[0]
                    # get the converted content
                    content_converted = transform_result_content.content_converted
                    # get the extension
                    extension = transform_result_content.content_extension
                    # get the type content by removing '.' from the extension
                    content_type = "text/" + extension.split(".")[1]

                return get_file_http_response(
                    content_converted,
                    data.title,
                    content_type,
                    extension,
                )
            else:
                return HttpResponseBadRequest("Error during the transformation ")

        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.DoesNotExist:
            content = {"message": document + " not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

""" REST Views for Exporters
"""
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

import core_exporters_app.commons.constants as exporter_constants
import core_exporters_app.components.exported_compressed_file.api as exported_compressed_file_api
import core_exporters_app.components.exporter.api as exporter_api
import core_main_app.components.data.api as data_api
from core_explore_common_app.components.result.models import Result
from core_exporters_app.components.exported_compressed_file.models import ExportedCompressedFile
from core_exporters_app.exporters.exporter import get_exporter_module_from_url, AbstractExporter
from core_exporters_app.rest.exporters.serializers import ExporterSerializer, ExporterExporterSerializer
from core_main_app.commons import exceptions
from core_main_app.utils.file import get_file_http_response


class ExporterList(APIView):
    """ List all Exporters
    """

    def get(self, request):
        """ Return http response with all exporters.

            GET /rest/exporter

            Args:
                request:

            Returns:

            """
        try:
            # Get object
            exporter_list = exporter_api.get_all(False)
            # Serialize object
            return_value = ExporterSerializer(exporter_list, many=True)
            # Return response
            return Response(return_value.data)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExporterDetail(APIView):
    """" Get an exporter
    """

    def get_object(self, pk):
        """ Retrieve an exporter

        Args:
            pk:

        Returns:

        """
        try:
            return exporter_api.get_by_id(pk)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """ Get xslt by its id.

        GET /rest/exporter/pk

        Args:
            request:
            pk:

        Returns:

        """
        try:
            # Get object
            exporter_object = self.get_object(pk)
            # Serialize object
            return_value = ExporterSerializer(exporter_object)
            # Return response
            return Response(return_value.data)
        except Http404:
            content = {'message': 'Exporter not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExportToZip(APIView):
    """ Export Data
    """

    def post(self, request):
        """ Generate a zip file

        POST /rest/exporter/export
        {
            "exporter_id_list": ["id", "id", ...],
            "data_id_list": ["id", "id", ...]
        }

        {
            "exporter_id_list":["5a81bcc08e4b10323d26b4dd", "5a81bcc08e4b10323d26b4de"],
            "data_id_list":["5a8314468e4b10dfbea6ffa4"]
        }

        Args:
            request:

        Returns:

        """
        try:
            # Build serializer
            export_serializer = ExporterExporterSerializer(data=request.data)
            # Validate xsl
            export_serializer.is_valid(True)
            # Creation of the compressed file with is_ready to false
            exported_file = ExportedCompressedFile(file_name='Query_Results.zip',
                                                   is_ready=False,
                                                   mime_type="application/zip")
            # Save in database to generate an Id and be accessible via url
            exported_file = exported_compressed_file_api.upsert(exported_file)

            # get all data
            data = data_api.get_by_id_list(request.data['data_id_list'], request.user)

            transformed_result_list = []
            for exporter_id in request.data['exporter_id_list']:
                # get the exporter with the given id
                exporter_object = exporter_api.get_by_id(exporter_id)
                # get the exporter module
                exporter_module = get_exporter_module_from_url(exporter_object.url)
                # if is a xslt transformation, we have to set the xslt
                if exporter_object.url == exporter_constants.XSL_URL:
                    # set the xslt
                    exporter_module.set_xslt(exporter_object.xsl_transformation.content)
                # transform the list of xml files
                transformed_result_list.extend(exporter_module.transform([Result(title=data_item.title,
                                                                                 xml_content=data_item.xml_content)
                                                                          for data_item in data]))
            # Export in Zip
            AbstractExporter.export(exported_file.id, transformed_result_list)
            content = {'message': 'the file is accessible for download at /rest/exporter/export/download/' +
                                  str(exported_file.id)}
            # return the Id to download the zip file
            return Response(content, status=status.HTTP_200_OK)
        except ValidationError as validation_exception:
            content = {'message': validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExporterDownload(APIView):
    """ Download a zip file
    """

    def get_object(self, pk):
        """ Retrieve an exported compressed file

        Args:
            pk:

        Returns:

        """
        try:
            return exported_compressed_file_api.get_by_id(pk)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """ Download the file

        GET /rest/exporter/download/pk

        Args:
            request:
            pk:

        Returns:

        """
        try:
            # Get object
            compressed_file_object = self.get_object(pk)
            if compressed_file_object.is_ready:
                return get_file_http_response(compressed_file_object.file.read(), compressed_file_object.file_name)
            else:
                content = {'message': 'The zip file is not yet ready.'}
                return Response(content, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            content = {'message': 'Compressed file not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

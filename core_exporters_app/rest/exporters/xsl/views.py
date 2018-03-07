""" REST Views for XSL Exporters
"""
from django.http import Http404
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

import core_exporters_app.components.exporter.api as exporter_api
import core_exporters_app.exporters.xsl.api as xsl_api
from core_exporters_app.rest.exporters.serializers import ExporterXslSerializer
from core_main_app.commons import exceptions
from core_main_app.utils.decorators import api_staff_member_required


class ExporterXslList(APIView):
    """ List all Xsl Exporters, or create.
    """

    def get(self, request):
        """ Return http response with all exporters.

            GET /rest/exporter/xsl

            Args:
                request:

            Returns:

            """
        try:
            # Get object
            exporter_list = xsl_api.get_all()
            # Serialize object
            return_value = ExporterXslSerializer(exporter_list, many=True)
            # Return response
            return Response(return_value.data)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @method_decorator(api_staff_member_required())
    def post(self, request):
        """ Save an exporter.

            POST /rest/exporter/xsl
            {
                "name": "exporter_name",
                "templates": ["id", "id"],
                "xsl_transformation": "id"
            }

            Args:
                request:

            Returns:

            """
        try:
            # Build serializer
            xsl_serializer = ExporterXslSerializer(data=request.data)
            # Validation
            xsl_serializer.is_valid(True)
            # save or update the object
            xsl_serializer.save()
            return Response(xsl_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as validation_exception:
            content = {'message': validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExporterXslDetail(APIView):
    """" Get Xsl exporter.
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
        """ Get exporter by its id.

        GET /rest/exporter/xsl/pk

        Args:
            request:
            pk:

        Returns:

        """
        try:
            # Get object
            xsl_object = self.get_object(pk)
            # Serialize object
            return_value = ExporterXslSerializer(xsl_object)
            # Return response
            return Response(return_value.data)
        except Http404:
            content = {'message': 'Xsl exporter not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

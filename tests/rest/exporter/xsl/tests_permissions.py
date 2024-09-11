""" Authentication tests for XSL Exporters REST API
"""

from django.test import SimpleTestCase
from unittest.mock import patch
from rest_framework import status

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock

import core_exporters_app.components.exporter.api as exporter_api
import core_exporters_app.exporters.xsl.api as xsl_api
from core_exporters_app.rest.exporters.serializers import ExporterXslSerializer
from core_exporters_app.rest.exporters.xsl import (
    views as xsl_exporters_api_views,
)


class TestExporterXslListGetPermissions(SimpleTestCase):
    """Test Exporter Xsl List Get Permissions"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_get(
            xsl_exporters_api_views.ExporterXslList.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(xsl_api, "get_all")
    @patch.object(ExporterXslSerializer, "data")
    def test_authenticated_returns_http_200(
        self, mock_exporter_serializer_data, mock_xsl_get_all
    ):
        """test_authenticated_returns_http_200"""

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            xsl_exporters_api_views.ExporterXslList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(xsl_api, "get_all")
    @patch.object(ExporterXslSerializer, "data")
    def test_staff_returns_http_200(
        self, mock_exporter_serializer_data, mock_xsl_get_all
    ):
        """test_staff_returns_http_200"""

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            xsl_exporters_api_views.ExporterXslList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestExporterXslListPostPermissions(SimpleTestCase):
    """Test Exporter Xsl List Post Permissions"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_post(
            xsl_exporters_api_views.ExporterXslList.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(ExporterXslSerializer, "is_valid")
    @patch.object(ExporterXslSerializer, "save")
    @patch.object(ExporterXslSerializer, "data")
    def test_authenticated_returns_http_403(
        self,
        mock_exporter_xsl_data,
        mock_exporter_xsl_save,
        mock_exporter_xsl_is_valid,
    ):
        """test_authenticated_returns_http_403"""

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            xsl_exporters_api_views.ExporterXslList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(ExporterXslSerializer, "is_valid")
    @patch.object(ExporterXslSerializer, "save")
    @patch.object(ExporterXslSerializer, "data")
    def test_staff_returns_http_201(
        self,
        mock_exporter_xsl_data,
        mock_exporter_xsl_save,
        mock_exporter_xsl_is_valid,
    ):
        """test_staff_returns_http_201"""

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_post(
            xsl_exporters_api_views.ExporterXslList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestExporterXslDetailGetPermissions(SimpleTestCase):
    """Test Exporter Xsl Detail Get Permissions"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_get(
            xsl_exporters_api_views.ExporterXslDetail.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(exporter_api, "get_by_id")
    @patch.object(ExporterXslSerializer, "data")
    def test_authenticated_returns_http_200(
        self, mock_exporter_data, mock_exporter_get_by_id
    ):
        """test_authenticated_returns_http_200"""

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            xsl_exporters_api_views.ExporterXslDetail.as_view(),
            mock_user,
            param={"pk": "0"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(exporter_api, "get_by_id")
    @patch.object(ExporterXslSerializer, "data")
    def test_staff_returns_http_200(
        self, mock_exporter_data, mock_exporter_get_by_id
    ):
        """test_staff_returns_http_200"""
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            xsl_exporters_api_views.ExporterXslDetail.as_view(),
            mock_user,
            param={"pk": "0"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

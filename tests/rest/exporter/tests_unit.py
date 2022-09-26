"""Units tests for exporter rest api
"""
from django.test import SimpleTestCase
from unittest.mock import patch
from rest_framework import status

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock

import core_exporters_app.rest.exporters.views as exporter_views
from core_exporters_app.components.exporter.models import Exporter


class TestGetExporterList(SimpleTestCase):
    """Test Get Exporter List"""

    def setUp(self):
        super().setUp()
        self.data = None

    @patch.object(Exporter, "get_all")
    def test_get_returns_status_200_with_no_permission_needed(
        self, mock_get_all
    ):
        """test_get_returns_status_200_with_no_permission_needed"""
        # Arrange
        user = create_mock_user("0")

        # Act
        response = RequestMock.do_request_get(
            exporter_views.ExporterList.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

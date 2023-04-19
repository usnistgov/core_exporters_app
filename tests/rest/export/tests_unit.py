"""Unit tests for exporter rest api
"""

from django.conf import settings
from unittest.mock import patch
from rest_framework import status


import core_main_app.components.data.api as data_api
from core_main_app.components.data.models import Data
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock

import core_exporters_app.rest.export.data.views as export_data_views
from tests.rest.export.fixtures.fixtures import ExportDataFixtures

fixture_data = ExportDataFixtures()


class TestExportDataById(IntegrationBaseTestCase):
    """Test Export Data By Id"""

    fixture = fixture_data

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = _create_data(self.fixture.template)

    def test_export_data_wrong_id_returns_http_404(self):
        """test_export_data_wrong_id_returns_http_404"""

        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            export_data_views.ExportData.as_view(),
            user,
            data={"data_id": -1, "exporter": "XML"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(data_api, "get_by_id")
    def test_export_data_wrong_exporter_returns_http_404(
        self, mock_data_api_get_by_id
    ):
        """test_export_data_wrong_exporter_returns_http_404"""

        # Arrange
        user = create_mock_user("1")
        mock_data_api_get_by_id.return_value = self.data

        # Act
        response = RequestMock.do_request_get(
            export_data_views.ExportData.as_view(),
            user,
            data={
                "data_id": mock_data_api_get_by_id.return_value.id,
                "exporter": "test",
            },
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(data_api, "get_by_id")
    def test_export_data_returns_status_200(self, mock_data_api_get_by_id):
        """test_export_data_returns_status_200"""

        # Arrange
        user = create_mock_user("1")
        mock_data_api_get_by_id.return_value = self.data

        # Act
        response = RequestMock.do_request_get(
            export_data_views.ExportData.as_view(),
            user,
            data={
                "data_id": mock_data_api_get_by_id.return_value.id,
                "exporter": self.fixture.exporter_xml.name,
            },
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


if "core_linked_records_app" in settings.INSTALLED_APPS:
    from core_linked_records_app.components.data import (
        api as linked_data_api,
    )

    class TestExportDataByPID(IntegrationBaseTestCase):
        """Test Export Data By PID"""

        fixture = fixture_data

        def setUp(self):
            """setUp"""

            super().setUp()
            self.data = _create_data(self.fixture.template)

        @patch.object(linked_data_api, "get_data_by_pid")
        def test_export_data_wrong_exporter_returns_http_404(
            self, mock_data_api_get_by_pid
        ):
            """test_export_data_wrong_exporter_returns_http_404"""

            # Arrange
            user = create_mock_user("1")

            mock_data_api_get_by_pid.return_value = self.data

            # Act
            response = RequestMock.do_request_get(
                export_data_views.ExportData.as_view(),
                user,
                data={
                    "data_pid": mock_data_api_get_by_pid.return_value.id,
                    "exporter": "test",
                },
            )

            # Assert
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        @patch.object(linked_data_api, "get_data_by_pid")
        def test_export_data_returns_status_200(
            self, mock_data_api_get_by_pid
        ):
            """test_export_data_returns_status_200"""

            # Arrange
            user = create_mock_user("1")
            mock_data_api_get_by_pid.return_value = self.data

            # Act
            response = RequestMock.do_request_get(
                export_data_views.ExportData.as_view(),
                user,
                data={
                    "data_pid": mock_data_api_get_by_pid.return_value.id,
                    "exporter": self.fixture.exporter_xml.name,
                },
            )

            # Assert
            self.assertEqual(response.status_code, status.HTTP_200_OK)


def _create_data(template, title="test"):
    """Create a data

    Args:
        template
        title:

    Returns:
    """
    data = Data(id=1, title=title, template=template, user_id="1")
    data.xml_content = '<root  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ><string>x</string></root>'
    return data

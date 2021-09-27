"""Unit tests for exporter rest api
"""

from rest_framework import status

import core_exporters_app.rest.export.data.views as export_data_views
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from tests.rest.export.fixtures.fixtures import ExportDataFixtures
from core_main_app.components.data.models import Data
from mock.mock import patch
import core_main_app.components.data.api as data_api
from django.conf import settings


fixture_data = ExportDataFixtures()


class TestExportDataById(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestExportDataById, self).setUp()
        self.data = _create_data(self.fixture.template)

    def test_export_data_wrong_id_returns_http_404(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            export_data_views.ExportData.as_view(),
            user,
            data={"data_id": "6111b84691cb057552b3da20", "exporter": "XML"},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(data_api, "get_by_id")
    def test_export_data_wrong_exporter_returns_http_404(self, mock_data_api_get_by_id):
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

    class TestExportDataByPID(MongoIntegrationBaseTestCase):
        fixture = fixture_data

        def setUp(self):
            super(TestExportDataByPID, self).setUp()
            self.data = _create_data(self.fixture.template)

        @patch.object(linked_data_api, "get_data_by_pid")
        def test_export_data_wrong_exporter_returns_http_404(
            self, mock_data_api_get_by_pid
        ):
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
        def test_export_data_returns_status_200(self, mock_data_api_get_by_pid):
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
    data = Data(title=title, template="6137af4b91cb055990297f35", user_id="1")
    data.id = "6111b84691cb057552b3da20"
    data.template = template
    data.xml_content = '<root  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ><string>x</string></root>'
    return data

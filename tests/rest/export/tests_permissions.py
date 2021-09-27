""" Authentication tests for Data Export REST API
"""
from django.test import SimpleTestCase
from mock.mock import patch
from rest_framework import status

from core_exporters_app.components.exporter.models import Exporter
import core_main_app.components.data.api as data_api
import core_exporters_app.components.exporter.api as exporter_api
from core_exporters_app.rest.export.data import views as export_api_views

from core_main_app.components.data.models import Data
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from core_main_app.components.template.models import Template


class TestExportDataByIdGetPermissions(SimpleTestCase):
    @patch.object(data_api, "get_by_id")
    @patch.object(exporter_api, "get_by_name")
    def test_anonymous_returns_http_200(
        self, mock_exporter_get_by_name, mock_data_api_get_by_id
    ):
        template = Template()
        mock_exporter_get_by_name.return_value = _create_exporter(template)
        mock_data_api_get_by_id.return_value = _create_data(template)
        response = RequestMock.do_request_get(
            export_api_views.ExportData.as_view(),
            AnonymousUser(),
            data={"data_id": "6111b84691cb057052b3da20", "exporter": "XML"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "get_by_id")
    @patch.object(exporter_api, "get_by_name")
    def test_authenticated_returns_http_200(
        self, mock_exporter_get_by_name, mock_data_api_get_by_id
    ):
        template = Template()
        mock_user = create_mock_user("1")
        mock_exporter_get_by_name.return_value = _create_exporter(template)
        mock_data_api_get_by_id.return_value = _create_data(template)

        response = RequestMock.do_request_get(
            export_api_views.ExportData.as_view(),
            mock_user,
            data={"data_id": "6111b84691cb057052b3da20", "exporter": "XML"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(data_api, "get_by_id")
    @patch.object(exporter_api, "get_by_name")
    def test_staff_returns_http_200(
        self, mock_exporter_get_by_name, mock_data_api_get_by_id
    ):
        template = Template()
        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)
        mock_exporter_get_by_name.return_value = _create_exporter(template)
        mock_data_api_get_by_id.return_value = _create_data(template)

        response = RequestMock.do_request_get(
            export_api_views.ExportData.as_view(),
            mock_user,
            data={"data_id": "6111b84691cb057052b3da20", "exporter": "XML"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


if "core_linked_records_app" in settings.INSTALLED_APPS:
    from core_linked_records_app.components.data import (
        api as linked_data_api,
    )

    class TestExportDataByPIDGetPermissions(SimpleTestCase):
        @patch.object(linked_data_api, "get_data_by_pid")
        @patch.object(exporter_api, "get_by_name")
        def test_anonymous_returns_http_200(
            self, mock_exporter_get_by_name, mock_data_api_get_by_pid
        ):
            template = Template()
            mock_exporter_get_by_name.return_value = _create_exporter(template)
            mock_data_api_get_by_pid.return_value = _create_data(template)
            response = RequestMock.do_request_get(
                export_api_views.ExportData.as_view(),
                AnonymousUser(),
                data={"data_pid": "6111b84691cb057052b3da20", "exporter": "XML"},
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

        @patch.object(linked_data_api, "get_data_by_pid")
        @patch.object(exporter_api, "get_by_name")
        def test_authenticated_returns_http_200(
            self, mock_exporter_get_by_name, mock_data_api_get_by_pid
        ):
            template = Template()
            mock_user = create_mock_user("1")
            mock_exporter_get_by_name.return_value = _create_exporter(template)
            mock_data_api_get_by_pid.return_value = _create_data(template)

            response = RequestMock.do_request_get(
                export_api_views.ExportData.as_view(),
                mock_user,
                data={"data_pid": "6111b84691cb057052b3da20", "exporter": "XML"},
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)

        @patch.object(linked_data_api, "get_data_by_pid")
        @patch.object(exporter_api, "get_by_name")
        def test_staff_returns_http_200(
            self, mock_exporter_get_by_name, mock_data_api_get_by_pid
        ):
            template = Template()
            mock_user = create_mock_user("1", is_staff=True, is_superuser=True)
            mock_exporter_get_by_name.return_value = _create_exporter(template)
            mock_data_api_get_by_pid.return_value = _create_data(template)

            response = RequestMock.do_request_get(
                export_api_views.ExportData.as_view(),
                mock_user,
                data={"data_pid": "6111b84691cb057052b3da20", "exporter": "XML"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)


def _create_exporter(
    template,
    name="XML",
    url="core_exporters_app.exporters.xml.models.XmlExporter",
):
    """Create an exporter

    Args:
        template:
        name:
        url:

    Returns:
    """

    return Exporter(name=name, url=url, enable_by_default=True, templates=[template])


def _create_data(
    template,
    title="test",
):
    """Create a data

    Args:
        template:
        title:

    Returns:
    """
    data = Data(title=title, template="6137af4b91cb055990297f35", user_id="1")
    data.template = template
    data.xml_content = '<root  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ><string>x</string></root>'
    return data

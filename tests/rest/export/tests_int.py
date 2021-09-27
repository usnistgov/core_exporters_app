"""Integration tests for exporter rest api
"""


import core_exporters_app.rest.export.data.views as export_data_views
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from tests.rest.export.fixtures.fixtures import ExportDataFixtures
from core_main_app.components.data.models import Data
from mock.mock import patch
import xmltodict
import json
import core_exporters_app.components.exporter.api as exporter_api
from core_main_app.components.xsl_transformation.models import XslTransformation

import core_main_app.components.data.api as data_api
from django.conf import settings


fixture_data = ExportDataFixtures()


class TestExportDataById(MongoIntegrationBaseTestCase):
    fixture = fixture_data

    def setUp(self):
        super(TestExportDataById, self).setUp()
        self.data = _create_data(self.fixture.template)

    @patch.object(data_api, "get_by_id")
    def test_export_data_with_xml_exporter_returns_the_transformed_data(
        self, mock_data_api_get_by_id
    ):
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
        self.assertXMLEqual(
            response.content.decode("utf-8"),
            mock_data_api_get_by_id.return_value.xml_content,
        )

    @patch.object(data_api, "get_by_id")
    def test_export_data_with_json_exporter_returns_the_transformed_data(
        self, mock_data_api_get_by_id
    ):
        # Arrange
        user = create_mock_user("1")
        mock_data_api_get_by_id.return_value = self.data

        # Act
        response = RequestMock.do_request_get(
            export_data_views.ExportData.as_view(),
            user,
            data={
                "data_id": mock_data_api_get_by_id.return_value.id,
                "exporter": self.fixture.exporter_json.name,
            },
        )

        # Assert
        data_dict = xmltodict.parse(mock_data_api_get_by_id.return_value.xml_content)
        expected_content = json.dumps(data_dict)

        self.assertJSONEqual(response.content.decode("utf-8"), expected_content)

    @patch.object(data_api, "get_by_id")
    @patch.object(exporter_api, "get_by_name")
    def test_export_data_with_xsl_exporter_returns_the_transformed_data(
        self, mock_exporter_get_by_name, mock_data_api_get_by_id
    ):
        # Arrange
        user = create_mock_user("1")
        self.fixture.exporter_xsl.xsl_transformation = _create_xsl_transform()
        mock_exporter_get_by_name.return_value = self.fixture.exporter_xsl
        mock_data_api_get_by_id.return_value = self.data

        # Act
        response = RequestMock.do_request_get(
            export_data_views.ExportData.as_view(),
            user,
            data={
                "data_id": mock_data_api_get_by_id.return_value.id,
                "exporter": self.fixture.exporter_xsl.name,
            },
        )

        # Assert, Check if the additional value has been created
        self.assertContains(response, "<additional>34</additional>")


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
        def test_export_data_with_xml_exporter_returns_the_transformed_data(
            self, mock_data_api_get_data_by_pid
        ):
            # Arrange
            user = create_mock_user("1")
            mock_data_api_get_data_by_pid.return_value = self.data

            # Act
            response = RequestMock.do_request_get(
                export_data_views.ExportData.as_view(),
                user,
                data={
                    "data_pid": mock_data_api_get_data_by_pid.return_value.id,
                    "exporter": self.fixture.exporter_xml.name,
                },
            )

            # Assert
            self.assertXMLEqual(
                response.content.decode("utf-8"),
                mock_data_api_get_data_by_pid.return_value.xml_content,
            )

        @patch.object(linked_data_api, "get_data_by_pid")
        def test_export_data_with_json_exporter_returns_the_transformed_data(
            self, mock_data_api_get_data_by_pid
        ):
            # Arrange
            user = create_mock_user("1")
            mock_data_api_get_data_by_pid.return_value = self.data

            # Act
            response = RequestMock.do_request_get(
                export_data_views.ExportData.as_view(),
                user,
                data={
                    "data_pid": mock_data_api_get_data_by_pid.return_value.id,
                    "exporter": self.fixture.exporter_json.name,
                },
            )

            # Assert
            data_dict = xmltodict.parse(
                mock_data_api_get_data_by_pid.return_value.xml_content
            )
            expected_content = json.dumps(data_dict)

            self.assertJSONEqual(response.content.decode("utf-8"), expected_content)

        @patch.object(linked_data_api, "get_data_by_pid")
        @patch.object(exporter_api, "get_by_name")
        def test_export_data_with_xsl_exporter_returns_the_transformed_data(
            self, mock_exporter_get_by_name, mock_data_api_get_data_by_pid
        ):
            # Arrange
            user = create_mock_user("1")
            self.fixture.exporter_xsl.xsl_transformation = _create_xsl_transform()
            mock_exporter_get_by_name.return_value = self.fixture.exporter_xsl
            mock_data_api_get_data_by_pid.return_value = self.data

            # Act
            response = RequestMock.do_request_get(
                export_data_views.ExportData.as_view(),
                user,
                data={
                    "data_pid": mock_data_api_get_data_by_pid.return_value.id,
                    "exporter": self.fixture.exporter_xsl.name,
                },
            )

            # Assert, Check if the additional value has been created
            self.assertContains(response, "<additional>34</additional>")


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
    data.xml_content = "<root  xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' ><test>value</test></root>"
    return data


def _create_xsl_transform():
    """Create xsl transform

    Args:


    Returns:
    """
    content = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">'
        "<!-- Identity transform -->"
        '<xsl:template match="@* | node()">'
        "<xsl:copy>"
        '         <xsl:apply-templates select="@* | node()"/>'
        "      </xsl:copy>"
        " </xsl:template>"
        ' <xsl:template match="test">'
        '     <xsl:copy-of select="."/>'
        "         <additional>34</additional>"
        "</xsl:template>"
        "</xsl:stylesheet>"
    )

    return XslTransformation(
        name="test_trans", filename="test_trans.xsl", content=content
    )

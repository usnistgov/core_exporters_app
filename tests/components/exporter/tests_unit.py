"""Units tests for exporter api
"""
from django.test import TestCase
from unittest.mock import patch
from core_main_app.commons import exceptions

import core_exporters_app.components.exporter.api as exporter_api
from core_exporters_app.components.exporter.models import Exporter


class TestExporterGetAllByUrl(TestCase):
    """Test Exporter Get All By Url"""

    @patch.object(Exporter, "get_all_by_url")
    def test_get_all_by_url_raises_error_when_does_not_exist(
        self, mock_get_all_by_url
    ):
        """test_get_all_by_url_raises_error_when_does_not_exist"""

        # Arrange
        mock_get_all_by_url.side_effect = exceptions.DoesNotExist("")

        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            exporter_api.get_all_by_url("url")

    @patch.object(Exporter, "get_all_by_url")
    def test_get_all_by_url_returns_list_exporters(self, mock_get_all_by_url):
        """test_get_all_by_url_returns_list_exporters"""

        # Arrange
        exporter = _create_mock_exporter()
        mock_get_all_by_url.return_value = [exporter]

        # Act
        result = exporter_api.get_all_by_url("url")

        # Assert
        self.assertEqual(len(result), 1)
        self.assertTrue(exporter in result)


class TestExporterGetAllByTemplateList(TestCase):
    """Test Exporter Get All By Template List"""

    def test_get_all_by_template_list_returns_empty_list(self):
        """test_get_all_by_template_list_returns_empty_list"""

        # Act
        result = exporter_api.get_all_by_template_list([2, 3])

        # Assert
        self.assertEqual(len(result), 0)

    @patch.object(Exporter, "get_all_by_template_list")
    def test_get_all_by_template_list_returns_list_exporters(
        self, mock_get_all_by_url
    ):
        """test_get_all_by_template_list_returns_list_exporters"""

        # Arrange
        exporter = _create_mock_exporter()
        mock_get_all_by_url.return_value = [exporter]

        # Act
        result = exporter_api.get_all_by_template_list([1])

        # Assert
        self.assertEqual(len(result), 1)
        self.assertTrue(exporter in result)


class TestExporterUpsert(TestCase):
    """Test Exporter Upsert"""

    @patch.object(Exporter, "save")
    def test_upsert_exporter_returns_exporter(self, mock_save):
        """test_upsert_exporter_returns_exporter

        Returns:

        """
        # Arrange
        exporter = _create_mock_exporter()
        mock_save.return_value = exporter

        # Act
        result = exporter_api.upsert(exporter)

        # Assert
        self.assertEqual(result, exporter)


def _create_mock_exporter():
    """_create_mock_exporter

    Returns:
    """
    return Exporter(name="exporter", url="url")

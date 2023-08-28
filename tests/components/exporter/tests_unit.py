"""Units tests for exporter api
"""
from unittest.mock import patch, MagicMock

from django.test import TestCase

import core_exporters_app.components.exporter.api as exporter_api
from core_exporters_app.components.exporter.models import Exporter
from core_exporters_app.components.exporter.watch import post_save_template
from core_main_app.commons import exceptions


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

    def test_get_all_by_template_list_with_empty_list_returns_empty_list(
        self,
    ):
        """test_get_all_by_template_list_with_empty_list_returns_empty_list"""
        # Act
        result = exporter_api.get_all_by_template_list([])

        # Assert
        self.assertEqual(len(result), 0)


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


class TestExporterGetNone(TestCase):
    """Test Exporter Upsert"""

    def test_exporter_get_none_returns_empty_list(self):
        """test_exporter_get_none_returns_empty_list

        Args:

        Returns:

        """
        # Act
        result = exporter_api.get_none()

        # Assert
        self.assertEqual(len(result), 0)


class TestPostSaveTemplate(TestCase):
    """Test Post Save Template"""

    @patch(
        "core_exporters_app.components.exporter.api.get_all_default_exporter"
    )
    def test_post_save_template_xsd_gets_all_exporters(
        self, mock_get_all_default_exporter
    ):
        """test_post_save_template_xsd_gets_all_exporters

        Args:

        Returns:

        """
        # Arrange
        mock_sender = MagicMock()
        mock_template = MagicMock(format="XSD")
        mock_all_default_exporters = MagicMock()
        mock_get_all_default_exporter.return_value = mock_all_default_exporters

        # Act
        post_save_template(sender=mock_sender, instance=mock_template)

        # Assert
        self.assertTrue(mock_get_all_default_exporter.called)
        self.assertFalse(mock_all_default_exporters.filter.called)

    @patch(
        "core_exporters_app.components.exporter.api.get_all_default_exporter"
    )
    def test_post_save_template_json_gets_filtered_exporters(
        self, mock_get_all_default_exporter
    ):
        """test_post_save_template_json_gets_filtered_exporters

        Args:

        Returns:

        """
        # Arrange
        mock_sender = MagicMock()
        mock_template = MagicMock(format="JSON")
        mock_all_default_exporters = MagicMock()
        mock_get_all_default_exporter.return_value = mock_all_default_exporters

        # Act
        post_save_template(sender=mock_sender, instance=mock_template)

        # Assert
        self.assertTrue(mock_get_all_default_exporter.called)
        self.assertTrue(mock_all_default_exporters.filter.called)

    @patch("core_exporters_app.components.exporter.api.get_none")
    @patch(
        "core_exporters_app.components.exporter.api.get_all_default_exporter"
    )
    def test_post_save_template_unknown_formats_gets_no_exporters(
        self, mock_get_all_default_exporter, mock_get_none
    ):
        """test_post_save_template_unknown_formats_gets_no_exporters

        Args:

        Returns:

        """
        # Arrange
        mock_sender = MagicMock()
        mock_template = MagicMock(format="UNKNOWN")

        # Act
        post_save_template(sender=mock_sender, instance=mock_template)

        # Assert
        self.assertFalse(mock_get_all_default_exporter.called)
        self.assertTrue(mock_get_none.called)


def _create_mock_exporter():
    """_create_mock_exporter

    Returns:
    """
    return Exporter(name="exporter", url="url")

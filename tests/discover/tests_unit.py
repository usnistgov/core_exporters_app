"""Exporters discover unit testing
"""

from unittest.case import TestCase
from unittest.mock import patch, MagicMock

from django.urls import re_path
from django.views import View

from core_exporters_app.exporters.discover import discover_exporter
from core_main_app.commons.exceptions import DoesNotExist


class TestDiscoverExporters(TestCase):
    """Test Discover Exporters"""

    def test_discover_exporters_without_urls_does_nothing(
        self,
    ):
        """test_discover_exporters_without_urls_does_nothing

        Returns:

        """
        self.assertIsNone(discover_exporter([]))

    @patch("core_exporters_app.components.exporter.api.upsert")
    @patch("core_exporters_app.components.exporter.api.get_by_url")
    def test_discover_exporters_with_a_url_saves_an_exporter(
        self, mock_get_exporter_by_id, mock_upsert_exporter
    ):
        """test_discover_exporters_with_a_url_saves_an_exporter

        Returns:

        """
        mock_get_exporter_by_id.side_effect = DoesNotExist("error")
        mock_upsert_exporter.return_value = MagicMock()
        discover_exporter(
            [
                re_path(
                    "exporter-test",
                    View,
                    {"name": "TEST", "enable_by_default": True},
                )
            ]
        )
        self.assertTrue(mock_upsert_exporter.called)

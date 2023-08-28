"""Units tests for blob exporter
"""
from unittest.mock import MagicMock, patch

from django.test import TestCase

from core_exporters_app.exporters.blob.models import BlobExporter


class TestBlobExporter(TestCase):
    """Test Blob Exporter"""

    @patch("core_main_app.utils.urls.get_blob_download_regex")
    def test_blob_exporter_transform_reads_result_content(
        self, mock_get_blob_download_regex
    ):
        """test_blob_exporter_transform_reads_result_content"""
        # Arrange
        mock_get_blob_download_regex.return_value = []

        # Act
        blob_exporter = BlobExporter()
        results = blob_exporter.transform(
            item_list=[MagicMock(title="data.xml", content="<root></root>")],
            session_key=None,
        )

        # Assert
        self.assertIsNotNone(results)

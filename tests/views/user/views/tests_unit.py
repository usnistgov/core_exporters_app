""" Unit tests for `core_exporters_app.views.user.views` package.
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_exporters_app.views.user import views as exporter_user_views
from core_main_app.commons.exceptions import DoesNotExist


class TestDownloadExportedCompressedFile(TestCase):
    """Unit tests for `download_exported_compressed_file` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {"request": MagicMock()}

        self.expected_assets = {
            "js": [
                {
                    "path": "core_exporters_app/user/js/exporter_compressed_file/download.js",
                    "is_raw": False,
                }
            ],
            "css": [],
        }

    @patch.object(exporter_user_views, "exported_file_api")
    def test_exported_file_api_get_by_id_called(self, mock_exported_file_api):
        """test_exported_file_api_get_by_id_called"""
        exporter_user_views.download_exported_compressed_file(
            **self.mock_kwargs
        )

        mock_exported_file_api.get_by_id.assert_called_with(
            self.mock_kwargs["request"].GET["id"],
            self.mock_kwargs["request"].user,
        )

    @patch.object(exporter_user_views, "exported_file_api")
    @patch.object(exporter_user_views, "render")
    def test_exported_file_api_get_by_id_does_not_exist_add_error_to_context(
        self, mock_render, mock_exported_file_api
    ):
        """test_exported_file_api_get_by_id_does_not_exist_add_error_to_context"""
        mock_exported_file_api.get_by_id.side_effect = DoesNotExist(
            "mock_exported_file_api_get_by_id_does_not_exist"
        )

        exporter_user_views.download_exported_compressed_file(
            **self.mock_kwargs
        )

        mock_render.assert_called_with(
            self.mock_kwargs["request"],
            "core_exporters_app/user/exported_compressed_file/download.html",
            context={
                "message": "The file with the given id does not exist.",
                "page_title": "Download Exported Files",
                "is_ready": False,
                "id_file": self.mock_kwargs["request"].GET["id"],
            },
            assets=self.expected_assets,
        )

    @patch.object(exporter_user_views, "exported_file_api")
    @patch.object(exporter_user_views, "render")
    def test_exported_file_api_get_by_id_exception_adds_error_to_context(
        self, mock_render, mock_exported_file_api
    ):
        """test_exported_file_api_get_by_id_exception_adds_error_to_context"""
        mock_exported_file_api.get_by_id.side_effect = Exception(
            "mock_exported_file_api_get_by_id_exception"
        )

        exporter_user_views.download_exported_compressed_file(
            **self.mock_kwargs
        )

        mock_render.assert_called_with(
            self.mock_kwargs["request"],
            "core_exporters_app/user/exported_compressed_file/download.html",
            context={
                "message": "Something went wrong while downloading. Please contact administrator.",
                "page_title": "Download Exported Files",
                "is_ready": False,
                "id_file": self.mock_kwargs["request"].GET["id"],
            },
            assets=self.expected_assets,
        )

    @patch.object(exporter_user_views, "exported_file_api")
    @patch.object(exporter_user_views, "HttpResponse")
    def test_exported_file_ready_returns_response(
        self, mock_http_response, mock_exported_file_api
    ):
        """test_exported_file_ready_returns_response"""
        mock_exported_file = MagicMock()
        mock_exported_file.is_ready = True
        mock_exported_file_api.get_by_id.return_value = mock_exported_file

        mock_http_response_object = MagicMock()
        mock_http_response.return_value = mock_http_response_object

        self.assertEqual(
            exporter_user_views.download_exported_compressed_file(
                **self.mock_kwargs
            ),
            mock_http_response_object,
        )

    @patch.object(exporter_user_views, "exported_file_api")
    @patch.object(exporter_user_views, "render")
    def test_exported_file_not_ready_returns_render(
        self, mock_render, mock_exported_file_api
    ):
        """test_exported_file_not_ready_returns_render"""
        mock_exported_file = MagicMock()
        mock_exported_file.is_ready = False
        mock_exported_file_api.get_by_id.return_value = mock_exported_file

        mock_render_output = MagicMock()
        mock_render.return_value = mock_render_output

        self.assertEqual(
            exporter_user_views.download_exported_compressed_file(
                **self.mock_kwargs
            ),
            mock_render_output,
        )

""" Test forms from `views.user.forms`.
"""
from unittest.case import TestCase
from unittest.mock import patch

from django.test import RequestFactory

from core_exporters_app.views.user.forms import ExportForm
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.template.models import Template
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestExportForm(TestCase):
    """Test Export Form"""

    def setUp(self):
        """setUp"""

        self.request = RequestFactory()
        self.request.user = create_mock_user(user_id="1", has_perm=True)

    @patch(
        "core_main_app.components.template.api.get_all_accessible_by_id_list"
    )
    def test_init_export_form_with_inaccessible_templates_raises_acl_error(
        self, mock_get_all_accessible_by_id_list
    ):
        """test_init_export_form_with_inaccessible_templates_raises_acl_error

        Returns:

        """
        mock_get_all_accessible_by_id_list.return_value = []

        with self.assertRaises(AccessControlError):
            ExportForm(
                request=self.request,
                template_id_list=["1", "2"],
                template_hash_list=[],
            )

    @patch(
        "core_main_app.components.template.api.get_all_accessible_by_id_list"
    )
    def test_init_export_form_with_accessible_and_inaccessible_templates_raises_acl_error(
        self, mock_get_all_accessible_by_id_list
    ):
        """test_init_export_form_with_accessible_and_inaccessible_templates_raises_acl_error

        Returns:

        """
        mock_get_all_accessible_by_id_list.return_value = [Template(id=1)]

        with self.assertRaises(AccessControlError):
            ExportForm(
                request=self.request,
                template_id_list=["1", "2"],
                template_hash_list=[],
            )

    @patch(
        "core_main_app.components.template.api.get_all_accessible_by_id_list"
    )
    @patch(
        "core_main_app.components.template.api.get_all_accessible_by_hash_list"
    )
    def test_init_export_form_with_accessible_templates_returns_form(
        self,
        mock_get_all_accessible_by_hash_list,
        mock_get_all_accessible_by_id_list,
    ):
        """test_init_export_form_with_accessible_templates_returns_form

        Returns:

        """
        mock_get_all_accessible_by_hash_list.return_value = []
        mock_get_all_accessible_by_id_list.return_value = [Template(id=1)]

        ExportForm(
            request=self.request, template_id_list=["1"], template_hash_list=[]
        )

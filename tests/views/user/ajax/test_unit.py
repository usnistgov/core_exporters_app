""" Unit tests for views from `views.user.ajax`.
"""
from unittest import TestCase

from django.http import HttpResponseBadRequest
from django.test import RequestFactory

from core_exporters_app.views.user import ajax as exporter_user_ajax

from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestOpenFormView(TestCase):
    """Unit tests for `open_form` method."""

    def setUp(self):
        """setUp"""
        factory = RequestFactory()

        self.request = factory.post("core_exporters_app_exporters_open_form")
        self.request.POST = {}
        self.request.user = create_mock_user(user_id="1", has_perm=True)

    def test_request_post_missing_params_returns_http_bad_request(self):
        """test_request_post_missing_params_returns_http_bad_request"""

        response = exporter_user_ajax.open_form(self.request)
        self.assertIsInstance(response, HttpResponseBadRequest)

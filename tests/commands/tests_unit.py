"""Exporter command unit testing
"""

from io import StringIO
from unittest.case import TestCase

from django.core.management import call_command


class TestLoadExportersCommand(TestCase):
    """Test Load Exporters command"""

    def test_command_output(self):
        out = StringIO()
        call_command("loadexporters", stdout=out)
        self.assertIn("Exporters were loaded in database.", out.getvalue())

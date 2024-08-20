"""Load exporters command
"""

from django.core.management.base import BaseCommand

from core_exporters_app.exporters import urls
from core_exporters_app.exporters.discover import discover_exporter


class Command(BaseCommand):
    help = "Reload exporters from list of installed apps"

    def handle(self, *args, **options):
        """handle

        Args:
            *args:
            **options:

        Returns:

        """
        discover_exporter(urls.urlpatterns)
        self.stdout.write(
            self.style.SUCCESS("Exporters were loaded in database.")
        )

""" Core exporters apps config
"""

import sys

from django.apps import AppConfig


class CoreExportersAppConfig(AppConfig):
    """Exporters configuration"""

    name = "core_exporters_app"
    verbose_name = "Core Exporters App"

    def ready(self):
        """Run once at startup"""
        if "migrate" not in sys.argv:
            import core_exporters_app.components.exporter.watch as exporter_watch
            from core_exporters_app.exporters import discover

            discover.init_periodic_tasks()
            exporter_watch.init()

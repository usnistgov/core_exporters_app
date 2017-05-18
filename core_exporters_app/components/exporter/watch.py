""" Handle Exporter signals
"""
from signals_utils.signals.mongo import connector, signals
from core_main_app.components.template.models import Template
import core_exporters_app.components.exporter.api as exporter_api


def init():
    """ Connect to template object events.
    """
    connector.connect(post_save_template, signals.post_save, sender=Template)


def post_save_template(sender, document, **kwargs):
    """ Method executed after a saving of a Template object.
    Args:
        document: template object.
        **kwargs:
    """
    default_exporter_list = exporter_api.get_all_default_exporter()

    for exporter in default_exporter_list:
        exporter.templates.append(document)
        exporter_api.upsert(exporter)

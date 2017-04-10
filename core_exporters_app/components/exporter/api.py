""" Exporter api
"""
from core_exporters_app.components.exporter.models import Exporter


def get_all():
    """ Lists all exporters

    Returns: exporter collection

    """
    return Exporter.get_all()


def get_by_id(exporter_id):
    """ Returns exporter object with the given id

    Args:
        exporter_id:

    Returns: exporter object

    """
    return Exporter.get_by_id(exporter_id)


def get_by_url(exporter_url):
    """ Returns exporter object with the given url

    Args:
        exporter_url:

    Returns: exporter object

    """
    return Exporter.get_by_url(exporter_url)


def upsert(exporter):
    """Saves or updates exporter

    Args:
        exporter:

    Returns:

    """
    return exporter.save()

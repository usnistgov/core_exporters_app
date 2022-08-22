""" Handle Exporter signals
"""
from django.db.models.signals import post_save, pre_delete

from core_main_app.components.template.models import Template
import core_exporters_app.components.exporter.api as exporter_api


def init():
    """Connect to template object events."""
    post_save.connect(post_save_template, sender=Template)
    pre_delete.connect(post_delete_template, sender=Template)


def post_save_template(sender, instance, **kwargs):
    """Method executed after saving of a Template object.
    Args:
        sender:
        instance: template object.
        **kwargs:
    """
    default_exporter_list = exporter_api.get_all_default_exporter()

    for exporter in default_exporter_list:
        # When an template is added, save is called 2 times
        # so we have to avoid to had the same instance several time
        if instance not in exporter.templates.all():
            exporter.templates.add(instance)
            exporter_api.upsert(exporter)


def post_delete_template(sender, instance, **kwargs):
    """Method executed after a template deletion.
        We are removing in all exporter, the reference to the deleted template
    Args:
        sender:
        instance:
        **kwargs:
    """
    exporter_list = exporter_api.get_all()
    for exporter in exporter_list:
        if instance in exporter.templates.all():
            exporter.templates.remove(instance)
            exporter_api.upsert(exporter)

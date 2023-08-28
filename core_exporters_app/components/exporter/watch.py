""" Handle Exporter signals
"""
from django.db.models.signals import post_save, pre_delete

import core_exporters_app.components.exporter.api as exporter_api
from core_main_app.components.template.models import Template


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
    # Check template format
    if instance.format == Template.XSD:
        default_exporter_list = exporter_api.get_all_default_exporter()
    elif instance.format == Template.JSON:
        default_exporter_list = exporter_api.get_all_default_exporter().filter(
            name=Template.JSON
        )
    else:
        default_exporter_list = exporter_api.get_none()

    for exporter in default_exporter_list:
        # When a template is added, save is called twice,
        # so we need to make sure we don't have the duplicates
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

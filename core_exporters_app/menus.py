""" Exporter app menu
"""
from django.urls import reverse
from menu import Menu, MenuItem


federated_children = (
    MenuItem(
        "Exporter List",
        reverse("core-admin:core_exporters_app_exporters"),
        icon="list",
    ),
)

Menu.add_item(
    "admin", MenuItem("EXPORTERS", None, children=federated_children)
)

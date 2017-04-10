""" views exporters app
"""
from django.contrib.admin.views.decorators import staff_member_required
from core_main_app.utils.rendering import admin_render
import core_exporters_app.components.exporter.api as exporter_api


@staff_member_required
def manage_exporters(request):
    """ Manage exporters, Display as list

    Args:
        request:

    Returns:

    """
    context = {
        'exporters_list': exporter_api.get_all()
    }

    modals = [
        "core_exporters_app/admin/exporters/list/modals/edit.html",
        "core_exporters_app/admin/exporters/list/modals/associated_templates.html"
    ]

    assets = {
        "js": [
            {
                "path": "core_main_app/libs/fSelect/js/fSelect.js",
                "is_raw": False
            },
            {
                "path": 'core_exporters_app/admin/js/exporters/list/modals/edit.js',
                "is_raw": False
            },
            {
                "path": 'core_exporters_app/admin/js/exporters/list/modals/associated_templates.js',
                "is_raw": False
            }
        ],
        "css": [
            "core_main_app/libs/fSelect/css/fSelect.css",
            "core_exporters_app/admin/css/exporters/list/list_exporters.css"
        ]
    }

    return admin_render(request,
                        'core_exporters_app/admin/exporters/list_exporters.html',
                        assets=assets,
                        context=context,
                        modals=modals)

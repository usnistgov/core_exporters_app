""" Ajax admin
"""
import json

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.urls import reverse_lazy
from django.utils.html import escape

import core_exporters_app.components.exporter.api as exporter_api
import core_main_app.components.template.api as template_api
from core_exporters_app.components.exporter.models import Exporter
from core_exporters_app.views.admin.forms import (
    AssociatedTemplatesForm,
    EditExporterForm,
)
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.views.common.ajax import EditObjectModalView


class EditExporterView(EditObjectModalView):
    form_class = EditExporterForm
    document = Exporter
    success_url = reverse_lazy("admin:core_exporters_app_exporters")
    success_message = "Exporter edited with success."

    def _save(self, form):
        # Save treatment.
        try:
            exporter_api.upsert(self.object)
        except Exception as e:
            form.add_error(None, str(e))


def associated_templates(request):
    """associated templates modal POST / GET

    Args:
        request:

    Returns:

    """
    try:
        if request.method == "POST":
            return _associated_templates_post(request)
        else:
            return _associated_templates_get(request)
    except AccessControlError as ace:
        return HttpResponseBadRequest("You don't have enough rights to do this.")
    except Exception as e:
        return HttpResponseBadRequest("An unexpected error occurred.")


def _associated_templates_post(request):
    """associated templates modal POST

    Args:
        request:

    Returns:

    """
    form = AssociatedTemplatesForm(request.POST, request=request)
    if form.is_valid():
        templates = request.POST.getlist("templates_manager", [])
        exporter_id = request.POST.get("id", None)
        if exporter_id is not None:
            exporter = exporter_api.get_by_id(exporter_id)
            template_id_list = [
                template_api.get(template_id, request=request)
                for template_id in templates
            ]
            exporter.templates = template_id_list
            exporter_api.upsert(exporter)
            return HttpResponse(json.dumps({}), content_type="application/javascript")
    else:
        return HttpResponseBadRequest("Bad entries. Please check your entries")


def _associated_templates_get(request):
    """associated templates modal GET

    Args:
        request:

    Returns:

    """
    context_params = dict()
    templates_selector = loader.get_template(
        "core_exporters_app/admin/exporters/list/associated_templates_base.html"
    )

    request_id = request.GET["exporter_id"]
    exporter = exporter_api.get_by_id(request_id)
    data_form = {
        "id": exporter.id,
        "templates_manager": [x.id for x in exporter.templates],
    }

    associated_form = AssociatedTemplatesForm(data_form, request=request)
    context_params["associated_form"] = associated_form
    context = {}
    context.update(request)
    context.update(context_params)
    return HttpResponse(
        json.dumps({"template": templates_selector.render(context)}),
        content_type="application/javascript",
    )

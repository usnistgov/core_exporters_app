""" Ajax admin
"""
import json

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.urls import reverse_lazy

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.views.common.ajax import EditObjectModalView

import core_exporters_app.commons.constants as exporter_constants
import core_exporters_app.components.exporter.api as exporter_api
import core_exporters_app.exporters.xsl.api as exporter_xsl_api
import core_main_app.components.template.api as template_api
from core_exporters_app.components.exporter.models import Exporter, ExporterXsl
from core_exporters_app.views.admin.forms import (
    AssociatedTemplatesForm,
    EditExporterForm,
)


class EditExporterView(EditObjectModalView):
    """Edit Exporter View"""

    form_class = EditExporterForm
    model = Exporter
    success_url = reverse_lazy("core-admin:core_exporters_app_exporters")
    success_message = "Exporter edited with success."

    def _save(self, form):
        # Save treatment.
        try:
            exporter_api.upsert(self.object)
        except Exception as exception:
            form.add_error(None, str(exception))


class EditExporterXslView(EditExporterView):
    """Edit Exporter Xsl View"""

    model = ExporterXsl


def associated_templates(request):
    """associated templates modal POST / GET

    Args:
        request:

    Returns:

    """
    try:
        if request.method == "POST":
            return _associated_templates_post(request)

        return _associated_templates_get(request)
    except AccessControlError:
        return HttpResponseBadRequest(
            "You don't have enough rights to do this."
        )
    except Exception:
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
            exporter = _get_exporter(exporter_id)
            template_id_list = [
                template_api.get_by_id(template_id, request=request)
                for template_id in templates
            ]
            exporter.templates.set(template_id_list)
            exporter_api.upsert(exporter)
            return HttpResponse(
                json.dumps({}), content_type="application/javascript"
            )
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

    exporter = _get_exporter(request_id)
    data_form = {
        "id": exporter.id,
        "templates_manager": [x.id for x in exporter.templates.all()],
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


def _get_exporter(exporter_id):
    """Returns exporter object with the given name

    Args:
        exporter_id:

    Returns: exporter object
    """
    exporter = exporter_api.get_by_id(exporter_id)
    # get the xsl exporter if it is an ExporterXSL object
    if exporter.url == exporter_constants.XSL_URL:
        exporter = exporter_xsl_api.get_by_id(exporter_id)

    return exporter

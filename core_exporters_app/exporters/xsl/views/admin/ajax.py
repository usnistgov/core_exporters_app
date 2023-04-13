""" XSLT ajax
"""
import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.template import loader
from django.utils.html import escape

import core_exporters_app.exporters.xsl.api as exporter_xsl_api
from core_exporters_app.exporters.xsl.views.admin.forms import (
    XsltSelectionForm,
)


@staff_member_required
def add_xslt(request):
    """add xslt modal POST / GET

    Args:
        request:

    Returns:

    """
    try:
        if request.method == "POST":
            return _add_xslt_post(request)

        return _add_xslt_get(request)
    except Exception as exception:
        return HttpResponseBadRequest(escape(str(exception)))


def _add_xslt_post(request):
    """add xslt modal POST

    Args:
        request:

    Returns:

    """
    try:
        if request.method == "POST":
            # get the form
            form = XsltSelectionForm(request.POST)
            if form.is_valid():
                # get the list of selected xslt
                xslt_list_selected = request.POST.getlist("xslt_list", None)
                if xslt_list_selected is None:
                    return HttpResponseBadRequest(
                        "Bad entries. Please check your entries"
                    )
                    # insert or delete xslt exporter
                exporter_xsl_api.upsert_or_delete_exporter_xsl(
                    xslt_list_selected
                )
                return HttpResponse(
                    json.dumps({}), content_type="application/javascript"
                )

            return HttpResponseBadRequest(
                "Bad entries. Please check your entries"
            )
    except Exception as exception:
        return HttpResponseBadRequest(
            escape(str(exception)), content_type="application/javascript"
        )


def _add_xslt_get(request):
    """add xslt modal GET

    Args:
        request:

    Returns:

    """
    try:
        context_params = dict()
        templates_selector = loader.get_template(
            "xsl/admin/exporters/list/add_base.html"
        )
        # get all xsl exporter
        exporter_xsl_list = exporter_xsl_api.get_all()
        # get all xsl id list from exporters xsl
        xslt_list = [
            exporter.xsl_transformation.id for exporter in exporter_xsl_list
        ]
        data_form = {"xslt_list": xslt_list}
        # set the list as data for pre selection
        xslt_form = XsltSelectionForm(data_form)
        context_params["xslt_selection_form"] = xslt_form
        context = {}
        context.update(request)
        context.update(context_params)
        return HttpResponse(
            json.dumps(
                {
                    "template": templates_selector.render(
                        context,
                    )
                }
            ),
            content_type="application/javascript",
        )
    except Exception:
        raise Exception("Error occurred during the form display")

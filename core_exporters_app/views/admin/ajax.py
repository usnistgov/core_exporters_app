""" Ajax admin
"""
import json

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.template import loader

import core_exporters_app.components.exporter.api as exporter_api
import core_main_app.components.template.api as template_api
from core_exporters_app.views.admin.forms import AssociatedTemplatesForm


def edit_exporter(request):
    """ Edit the exporter

    Args:
        request:

    Returns:

    """
    try:
        exporter = exporter_api.get_by_id(request.POST['id'])
        exporter.name = request.POST['title']
        exporter_api.upsert(exporter)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')
    return HttpResponse(json.dumps({}), content_type='application/javascript')


def associated_templates(request):
    """ associated templates modal POST / GET

    Args:
        request:

    Returns:

    """
    try:
        if request.method == 'POST':
            return _associated_templates_post(request)
        else:
            return _associated_templates_get(request)
    except Exception as e:
        return HttpResponseBadRequest(e.message)


def _associated_templates_post(request):
    """ associated templates modal POST

    Args:
        request:

    Returns:

    """
    try:
        form = AssociatedTemplatesForm(request.POST)
        if form.is_valid():
            templates = request.POST.getlist('templates_manager', [])
            exporter_id = request.POST.get('id', None)
            if exporter_id is not None:
                exporter = exporter_api.get_by_id(exporter_id)
                template_id_list = [template_api.get(template_id) for template_id in templates]
                exporter.templates = template_id_list
                exporter_api.upsert(exporter)
                return HttpResponse(json.dumps({}), content_type='application/javascript')
        else:
            return HttpResponseBadRequest('Bad entries. Please check your entries')
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')


def _associated_templates_get(request):
    """ associated templates modal GET

    Args:
        request:

    Returns:

    """
    try:
        context_params = dict()
        templates_selector = \
            loader.get_template('core_exporters_app/admin/exporters/list/associated_templates_base.html')

        request_id = request.GET['exporter_id']
        exporter = exporter_api.get_by_id(request_id)
        data_form = {'id': exporter.id, 'templates_manager': [x.id for x in exporter.templates]}

        associated_form = AssociatedTemplatesForm(data_form)
        context_params['associated_form'] = associated_form
        context = {}
        context.update(request)
        context.update(context_params)
        return HttpResponse(json.dumps({'template': templates_selector.render(context)}),
                            content_type='application/javascript')
    except Exception as e:
        raise Exception('Error occurred during the form display')

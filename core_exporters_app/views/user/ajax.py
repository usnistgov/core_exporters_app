""" Ajax Exporter user
"""
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseBadRequest
from core_explore_common_app.components.result.models import Result
from core_explore_common_app.rest.result.serializers import ResultBaseSerializer
from django.template import RequestContext, loader
from core_exporters_app.views.user.forms import ExportForm
from core_exporters_app.exporters.exporter import get_exporter_module_from_url, AbstractExporter
import core_exporters_app.commons.constants as exporter_constants
import core_exporters_app.components.exported_compressed_file.api as exported_file_api
import core_exporters_app.components.exporter.api as exporter_api
import requests
import json


def exporters_selection(request):
    """ exporters selection modal POST / GET

    Args:
        request:

    Returns:

    """
    try:
        if request.method == 'POST':
            return _exporters_selection_post(request)
        else:
            return _exporters_selection_get(request)
    except Exception as e:
        return HttpResponseBadRequest(e.message)


def check_download_status(request):
    """ Checks if a file is ready for download, Id is expected on the request

    Args:
        request:

    Returns:

    """
    file_id = request.GET.get('file_id', None)

    if file_id is not None:
        try:
            # Get the exported file with the given id
            exported_file = exported_file_api.get_by_id(file_id)
        except:
            return HttpResponseBadRequest("File with the given id does not exist")

        return HttpResponse(json.dumps({'is_ready': exported_file.is_ready,
                                        'message': "The file is now ready for download"}),
                            content_type='application/javascript')
    else:
        return HttpResponseBadRequest("File id is missing in parameters")


def _exporters_selection_post(request):
    """ exporters selection modal POST

    Args:
        request:

    Returns:

    """
    try:
        if request.method == 'POST':
            # gets all parameters
            templates_id = request.POST['templates_id'].split(',')
            data_url_list = request.POST['data_url_list'].split(',')
            form = ExportForm(request.POST, templates_id=templates_id, data_url_list=data_url_list)
            url_base = request.build_absolute_uri('/')[:-1]
            if form.is_valid():
                exporters = request.POST.getlist('my_exporters', None)
                if exporters is not None:
                    # gets all data from the url list
                    result_list = _get_results_list_from_url_list(url_base, data_url_list)
                    # start the export
                    exported_compressed_file_id = _export_result(exporters, result_list)
                    # generates the redirect link for download the file
                    url_download = reverse("core_exporters_app_exporters_download")
                    url_to_redirect = "{0}{1}?id={2}".format(url_base, url_download, str(exported_compressed_file_id))
                    return HttpResponse(json.dumps({'url_to_redirect': url_to_redirect}),
                                        content_type='application/json')
            else:
                return HttpResponseBadRequest('Bad entries. Please check your entries')
        else:
            return HttpResponseBadRequest('Bad entries. Please check your entries')
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')


def _exporters_selection_get(request):
    """ exporters selection modal GET

    Args:
        request:

    Returns:

    """
    try:
        context_params = dict()

        # Template form base
        templates_selector = \
            loader.get_template('core_exporters_app/user/exporters/list/list_exporters_selector_base.html')

        # Getting the template ID list and data selected URL because the Export Form need it
        templates_list = request.GET.getlist('templates_list[]')
        data_url_list = request.GET.getlist('data_url_list[]')

        # Generating the Export form
        exporters_selection_form = ExportForm(templates_id=templates_list, data_url_list=data_url_list)
        context_params['exporters_selector_form'] = exporters_selection_form

        # Generates and returns the context
        context = RequestContext(request, context_params)
        return HttpResponse(json.dumps({'template': templates_selector.render(context)}),
                            content_type='application/javascript')
    except Exception as e:
        raise Exception('Error occurred during the form display')


def _get_results_list_from_url_list(url_base, url_list):
    """ Gets all data from url

    Args:
        url_base: url of running server
        url_list: url list to request

    Returns:

    """
    result_list = []
    for url in url_list:
        response = requests.get(url_base + url)
        if response.status_code == 200:
            # Build serializer
            results_serializer = ResultBaseSerializer(data=json.loads(response.text))
            # Validate result
            results_serializer.is_valid(True)
            # Append the list returned
            result_list.append(Result(title=results_serializer.data['title'],
                                      xml_content=results_serializer.data['xml_content']))
    return result_list


def _export_result(exporters_list_url, result_list):
    """ Exports all result

    Args:
        exporters_list_url:
        result_list:

    Returns:

    """
    transformed_result_list = []

    # Converts all data
    for exporter_id in exporters_list_url:
        # get the exporter with the given id
        exporter_object = exporter_api.get_by_id(exporter_id)
        # get the exporter module
        exporter_module = get_exporter_module_from_url(exporter_object.url)
        # if is a xslt transformation, we have to set the xslt
        if exporter_object.url == exporter_constants.XSL_URL:
            # set the xslt
            exporter_module.set_xslt(exporter_object.xsl_transformation.content)
        # transform the list of xml files
        transformed_result_list.append(exporter_module.transform(result_list))

    # Export in Zip
    exported_compressed_file_id = AbstractExporter.export(transformed_result_list)
    return exported_compressed_file_id

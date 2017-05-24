""" Exporter forms
"""
from django import forms
import core_exporters_app.components.exporter.api as exporters_api
import core_main_app.components.template.api as template_api


class ExportForm(forms.Form):
    """ Create the form for exporting data
    """
    my_exporters = forms.MultipleChoiceField(label='', choices=[],
                                             widget=forms.CheckboxSelectMultiple(), required=True)

    export_options = []

    def __init__(self, *args, **kwargs):
        """ Init the form

        Args:
            templates_id:
            data_url_list:
        """
        self.export_options = []
        self.data_url_list = []
        self.templates_id = []

        if 'templates_id' in kwargs:
            self.templates_id = kwargs.pop('templates_id')
            # Retrieves all corresponded template
            templates = template_api.get_all_by_id_list(self.templates_id)
            # Retrieves all common exporter for exporters given
            exporters = exporters_api.get_all_by_template_list(templates)
            for exporter in exporters:
                self.export_options.append((exporter.id, exporter.name))

        if 'data_url_list' in kwargs:
            self.data_url_list = kwargs.pop('data_url_list')

        super(ExportForm, self).__init__(*args, **kwargs)
        self.fields['my_exporters'].choices = self.export_options

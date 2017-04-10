""" Forms admin exporter
"""
from django import forms
from core_main_app.components.template_version_manager import api as template_version_manager_api


class AssociatedTemplatesForm(forms.Form):
    """ Associated Template form
    """
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    templates_manager = forms.MultipleChoiceField(label='', widget=forms.SelectMultiple(), required=False)

    def __init__(self, *args, **kwargs):
        super(AssociatedTemplatesForm, self).__init__(*args, **kwargs)
        self.fields['templates_manager'].choices = _get_templates_versions()


def _get_templates_versions():
    """ Get templates versions.

    Returns:
        List of templates versions.

    """
    templates = []
    try:
        list_ = template_version_manager_api.get_active_global_version_manager()
        for elt in list_:
            for version in elt.versions:
                version_name = "{0} (Version {1})".format(elt.title,
                                                          template_version_manager_api.get_version_number(elt, version))
                templates.append((version, version_name))
    except Exception:
        pass

    return templates

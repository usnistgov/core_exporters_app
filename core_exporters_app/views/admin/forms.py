""" Forms admin exporter
"""
from django import forms
from django.forms import ModelForm

from core_exporters_app.components.exporter.models import Exporter
from core_main_app.components.template import api as template_api


class EditExporterForm(ModelForm):
    """Edit Exporter Form"""

    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Type the new name"}
        ),
    )

    class Meta:
        """Meta"""

        model = Exporter
        fields = ["name"]


class AssociatedTemplatesForm(forms.Form):
    """Associated Template form"""

    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    templates_manager = forms.MultipleChoiceField(
        label="",
        widget=forms.CheckboxSelectMultiple(attrs={"class": "double-columns"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields["templates_manager"].choices = _get_templates_versions(
            request=request
        )


def _get_templates_versions(request):
    """Get templates versions.

    Args:
        request:

    Returns:
        List of template versions

    """
    templates = []
    # display all template, global and from users
    template_list = template_api.get_all(request=request)
    for template in template_list:
        templates.append((template.id, template.display_name))
    return templates

""" Exporter model
"""
from django_mongoengine import fields, Document
from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
import core_main_app.components.version_manager.api as version_manager_api
from mongoengine import errors as mongoengine_errors


class Exporter(Document):
    """Represents an exporter"""
    name = fields.StringField(blank=False, unique=True)
    url = fields.StringField(blank=False)
    enable_by_default = fields.BooleanField(blank=False)
    templates = fields.ListField(fields.ReferenceField(Template), blank=True)

    @staticmethod
    def get_all():
        """ Returns all exporters

        Returns:
            exporter collection

        """
        return Exporter.objects().all()

    @staticmethod
    def get_all_default_exporter():
        """ Lists all default exporters

        Returns: exporter collection

        """
        return Exporter.objects(enable_by_default=True).all()

    @staticmethod
    def get_all_by_template_list(template_id_list):
        """ Gets all template matching with the given list template id

        Args:
            template_id_list:

        Returns:

        """
        return Exporter.objects(templates__in=template_id_list).all()

    @staticmethod
    def get_by_id(exporter_id):
        """ Returns the object with the given id

        Args:
            exporter_id:

        Returns:
            Exporter (obj): Exporter object with the given id

        """
        try:
            return Exporter.objects.get(pk=str(exporter_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as ex:
            raise exceptions.ModelError(ex.message)

    @staticmethod
    def get_by_url(exporter_url):
        """ Returns the object with the given url

        Args:
            exporter_url:

        Returns:
            Exporter (obj): Exporter object with the given url

        """
        try:
            return Exporter.objects.get(url=exporter_url)
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as ex:
            raise exceptions.ModelError(ex.message)

    def get_templates_to_string(self):
        """ To string value for exporter's template list

        Returns:

        """
        version_name_list = []
        for template in self.templates:
            version_manager = version_manager_api.get_from_version(template)
            version_number = version_manager_api.get_version_number(version_manager, template.id)
            version_name = "{0} (Version {1})".format(version_manager.title,
                                                      version_number)
            version_name_list.append(version_name)

        return_value = ", ".join(version_name_list)
        return return_value

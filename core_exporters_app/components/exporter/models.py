""" Exporter model
"""
from mongoengine import errors as mongoengine_errors
from mongoengine.queryset.base import PULL

from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_main_app.utils.validation.regex_validation import not_empty_or_whitespaces
from django_mongoengine import fields, Document


class Exporter(Document):
    """Represents an exporter"""

    meta = {"allow_inheritance": True}

    name = fields.StringField(
        blank=False, unique=True, validation=not_empty_or_whitespaces
    )
    url = fields.StringField(blank=False)
    enable_by_default = fields.BooleanField(blank=False)
    templates = fields.ListField(
        fields.ReferenceField(Template), blank=True, reverse_delete_rule=PULL
    )

    @staticmethod
    def get_all(is_cls):
        """Returns all exporters

        Returns:
            exporter collection

        """
        if is_cls:
            # will return all Exporter object only
            return Exporter.objects(_cls=Exporter.__name__).all()
        else:
            # will return all inherited object
            return Exporter.objects().all()

    @staticmethod
    def get_all_by_url(url):
        """Lists all exporters with the given url

        Args:
            url:

        Returns:

        """
        return Exporter.objects(url=url).all()

    @staticmethod
    def get_all_default_exporter():
        """Lists all default exporters

        Returns: exporter collection

        """
        return Exporter.objects(enable_by_default=True).all()

    @staticmethod
    def get_all_by_template_list(template_id_list):
        """Gets all template matching with the given list template id

        Args:
            template_id_list:

        Returns:

        """
        return Exporter.objects(templates__all=template_id_list).all()

    @staticmethod
    def get_by_id(exporter_id):
        """Returns the object with the given id

        Args:
            exporter_id:

        Returns:
            Exporter (obj): Exporter object with the given id

        """
        try:
            return Exporter.objects.get(pk=str(exporter_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_by_url(exporter_url):
        """Returns the object with the given url

        Args:
            exporter_url:

        Returns:
            Exporter (obj): Exporter object with the given url

        """
        try:
            return Exporter.objects.get(url=exporter_url)
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    def get_templates_to_string(self):
        """To string value for exporter's template list

        Returns:

        """
        version_name_list = []
        for template in self.templates:
            version_name_list.append(template.display_name)

        return_value = ", ".join(version_name_list)
        return return_value

    def save_object(self):
        """Custom save

        Returns:

        """
        try:
            return self.save()
        except mongoengine_errors.NotUniqueError as e:
            raise exceptions.NotUniqueError(
                "The name is already used by an other exporter."
            )
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    def clean(self):
        """Clean is called before saving

        Returns:

        """
        self.name = self.name.strip()

""" Exporter model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import models, IntegrityError

from core_main_app.commons import exceptions
from core_main_app.commons.regex import NOT_EMPTY_OR_WHITESPACES
from core_main_app.components.template.models import Template
from core_main_app.components.xsl_transformation.models import XslTransformation


class Exporter(models.Model):
    """Represents an exporter"""

    class_name = "Exporter"

    name = models.CharField(
        blank=False,
        validators=[
            RegexValidator(
                regex=NOT_EMPTY_OR_WHITESPACES,
                message="Title must not be empty or only whitespaces",
                code="invalid_title",
            ),
        ],
        max_length=200,
        unique=True,
    )
    url = models.CharField(blank=False, max_length=200)
    enable_by_default = models.BooleanField(blank=False)
    templates = models.ManyToManyField(
        Template,
        blank=True,
    )
    _cls = models.CharField(default="Exporter", max_length=200)

    @staticmethod
    def get_all(is_cls):
        """Returns all exporters

        Returns:
            exporter collection

        """
        if is_cls:
            # will return all Exporter object only
            return Exporter.objects.filter(_cls=Exporter.class_name).all()
        else:
            # will return all inherited object
            return Exporter.objects.all()

    @staticmethod
    def get_all_by_url(url):
        """Lists all exporters with the given url

        Args:
            url:

        Returns:

        """
        return Exporter.objects.filter(url=url).all()

    @staticmethod
    def get_all_default_exporter():
        """Lists all default exporters

        Returns: exporter collection

        """
        return Exporter.objects.filter(enable_by_default=True).all()

    @staticmethod
    def get_all_by_template_list(template_id_list):
        """Gets all template matching with the given list template id

        Args:
            template_id_list:

        Returns:

        """
        queryset = Exporter.objects.all()
        for pk in template_id_list:
            queryset = queryset.filter(templates=pk)
        return queryset.all()  # TODO: test if works to replace __all

    def has_template(self, template):
        """Check if exporter has template

        Args:
            template:

        Returns:

        """
        return self.templates.filter(id=template.id).exists()

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
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_by_name(exporter_name):
        """Returns the object with the given name

        Args:
            exporter_name:

        Returns:
            Exporter (obj): Exporter object with the given name

        """
        try:
            return Exporter.objects.get(name=str(exporter_name))
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
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
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    def get_templates_to_string(self):
        """To string value for exporter's template list

        Returns:

        """
        version_name_list = []
        for template in self.templates.all():
            version_name_list.append(template.display_name)

        return_value = ", ".join(version_name_list)
        return return_value

    def save_object(self):
        """Custom save

        Returns:

        """
        try:
            self._cls = self.class_name
            return self.save()
        except IntegrityError:
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

    def __str__(self):
        """

        Returns:

        """
        return self.name


class ExporterXsl(Exporter):
    """Export XSL object"""

    class_name = "ExporterXsl"

    xsl_transformation = models.ForeignKey(
        XslTransformation, blank=False, on_delete=models.CASCADE
    )

    @staticmethod
    def get_all(is_cls):
        """Returns all XSL exporters

        Returns:
            XSL exporter collection

        """
        if is_cls:
            # will return all Template object only
            return ExporterXsl.objects.filter(_cls=ExporterXsl.class_name).all()
        else:
            # will return all inherited object
            return ExporterXsl.object.all()

    @staticmethod
    def get_all_by_xsl_id_list(xsl_id_list):
        """Returns all Xsl exporter with the given id list

        Returns:

        """
        return ExporterXsl.objects.filter(xsl_transformation__in=xsl_id_list).all()

    @staticmethod
    def get_by_name(exporter_xsl_name):
        """Returns the object with the given name

        Args:
            exporter_xsl_name:

        Returns:
            Exporter Xsl (obj): exporter xsl object with the given name

        """
        try:
            return ExporterXsl.objects.get(name=str(exporter_xsl_name))
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))

        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_by_id(exporter_xsl_id):
        """Returns the object with the given id

        Args:
            exporter_xsl_id:

        Returns:
            Exporter Xsl (obj): Exporter xsl object with the given id

        """
        try:
            return ExporterXsl.objects.get(pk=str(exporter_xsl_id))
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

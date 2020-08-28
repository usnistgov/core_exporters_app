""" XSLT exporter
"""
import logging

from django_mongoengine import fields
from mongoengine.queryset.base import CASCADE

import xml_utils.commons.exceptions as exceptions
from core_exporters_app.components.exporter.models import Exporter
from core_exporters_app.exporters.exporter import (
    AbstractExporter,
    TransformResult,
    TransformResultContent,
)
from core_main_app.components.xsl_transformation.models import XslTransformation
from xml_utils.xsd_tree.xsd_tree import XSDTree

logger = logging.getLogger(__name__)


class XslExporter(AbstractExporter):
    """XSLT Exporter module. generate the XML results"""

    def __init__(self):
        """Sets the default name and extension"""
        self.name = "XSLT"
        # default extension
        self.extension = ".xml"
        self.xslt = None
        self.transformation = None

    def set_xslt(self, xsl_transformation):
        """Set the XSLT to use for the transformation.

        Args:
            xsl_transformation:

        Returns:

        """
        # set the name
        self.name = xsl_transformation.name
        # set the xslt
        self.xslt = xsl_transformation.content
        # parse the xslt
        xslt_parsed = XSDTree.build_tree(xsl_transformation.content)
        # set the extension
        self._set_extension_from_xslt(xslt_parsed)
        # set the transform
        self.transformation = XSDTree.transform_to_xslt(xslt_parsed)

    def transform(self, xml_inputs, session_key):
        """Transforms the input to a json content

        Args:
            xml_inputs: xml files
            session_key: session key

        Returns:

        """
        results_transform = []
        # loops on all xml input
        for xml_item in xml_inputs:
            # generate the title document with the sha
            document_name_with_sha = AbstractExporter.get_title_document(
                xml_item["title"], xml_item["xml_content"]
            )
            transform_result = TransformResult()
            # set the document name to the collection
            transform_result.source_document_name = "{!s}.{!s}".format(
                document_name_with_sha, self.name
            )
            # for an XML transformation there is a list of one element
            transform_result_content = TransformResultContent()
            transform_result_content.file_name = document_name_with_sha
            # sets the content and extension
            dom = XSDTree.transform_to_xml(xml_item["xml_content"])
            transform_result_content.content_converted = str(self.transformation(dom))
            transform_result_content.content_extension = self.extension
            # add the content to the list of content
            transform_result.transform_result_content.append(transform_result_content)
            # add the result to the list of result
            results_transform.append(transform_result)
        return results_transform

    def _set_extension_from_xslt(self, xslt):
        """Define the extension from the xslt

        Args:
            xslt:

        Returns:

        """
        extension_result = None

        try:
            extension_result = XSDTree.get_extension(xslt)
        except exceptions.XMLError as e:
            logger.error(
                "It is not possible to determine the output format, xml by default will be used: {0}".format(
                    str(e)
                )
            )

        if extension_result:
            self.extension = ".{!s}".format(extension_result)


class ExporterXsl(Exporter):
    """Export XSL object"""

    xsl_transformation = fields.ReferenceField(
        XslTransformation, blank=False, reverse_delete_rule=CASCADE
    )

    @staticmethod
    def get_all(is_cls):
        """Returns all XSL exporters

        Returns:
            XSL exporter collection

        """
        if is_cls:
            # will return all Template object only
            return ExporterXsl.objects(
                _cls="{0}.{1}".format(Exporter.__name__, ExporterXsl.__name__)
            ).all()
        else:
            # will return all inherited object
            return ExporterXsl.object().all()

    @staticmethod
    def get_all_by_xsl_id_list(xsl_id_list):
        """Returns all Xsl exporter with the given id list

        Returns:

        """
        return ExporterXsl.objects(xsl_transformation__in=xsl_id_list).all()

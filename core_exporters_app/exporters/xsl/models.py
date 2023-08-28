""" XSLT exporter
"""
import logging

from xml_utils.commons import exceptions
from xml_utils.xsd_tree.xsd_tree import XSDTree

from core_exporters_app.exporters.exporter import (
    AbstractExporter,
    TransformResult,
    TransformResultContent,
)

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

    def transform(self, item_list, session_key):
        """Transforms the input to a json content

        Args:
            item_list: xml files
            session_key: session key

        Returns:

        """
        results_transform = []
        # loops on all xml input
        for item in item_list:
            # generate the title document with the sha
            document_name_with_sha = AbstractExporter.get_title_document(
                item.title, item.content
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
            dom = XSDTree.transform_to_xml(item.content)
            transform_result_content.content_converted = str(
                self.transformation(dom)
            )
            transform_result_content.content_extension = self.extension
            # add the content to the list of content
            transform_result.transform_result_content.append(
                transform_result_content
            )
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
        except exceptions.XMLError as exception:
            logger.error(
                "It is not possible to determine the output format, "
                "xml by default will be used: %s",
                str(exception),
            )

        if extension_result:
            self.extension = ".{!s}".format(extension_result)

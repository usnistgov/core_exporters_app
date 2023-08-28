""" XML exporter
"""
from core_exporters_app.exporters.exporter import (
    AbstractExporter,
    TransformResult,
    TransformResultContent,
)


class XmlExporter(AbstractExporter):
    """XML Exporter. generate the XML results"""

    def __init__(self):
        """Sets the default name and extension"""
        self.name = "XML"
        self.extension = ".xml"

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
            transform_result.source_document_name = document_name_with_sha
            # for an XML transformation there is a list of one element
            transform_result_content = TransformResultContent()
            transform_result_content.file_name = document_name_with_sha
            # sets the content
            transform_result_content.content_converted = item.content
            # sets the extension
            transform_result_content.content_extension = self.extension
            # add the content to the list of content
            transform_result.transform_result_content.append(
                transform_result_content
            )
            # add the result to the list of result
            results_transform.append(transform_result)
        return results_transform

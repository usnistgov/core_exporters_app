""" Json exporter
"""
import json
from json.decoder import JSONDecodeError

from core_main_app.settings import XML_POST_PROCESSOR, XML_FORCE_LIST
from core_main_app.utils import xml as xml_utils
from core_exporters_app.exporters.exporter import (
    AbstractExporter,
    TransformResult,
    TransformResultContent,
)


class JsonExporter(AbstractExporter):
    """JSON Exporter. Allows to transform an XML to a JSON"""

    def __init__(self):
        self.name = "JSON"
        self.extension = ".json"

    def transform(self, item_list, session_key):
        """Transforms the input to a json content

        Args:
            item_list:
            session_key:

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
            # for an JSON transformation there is a list of one element
            transform_result_content = TransformResultContent()
            transform_result_content.file_name = document_name_with_sha
            # Transform to JSON
            try:
                transformed_content = json.loads(item.content)
            except JSONDecodeError:
                transformed_content = xml_utils.raw_xml_to_dict(
                    item.content,
                    postprocessor=XML_POST_PROCESSOR,
                    force_list=XML_FORCE_LIST,
                )
            # sets the content and extension
            try:
                transform_result_content.content_converted = json.dumps(
                    transformed_content, indent=4, ensure_ascii=False
                )
            except Exception:
                transform_result_content.content_converted = json.dumps(
                    transformed_content, indent=4
                )

            transform_result_content.content_extension = self.extension
            # add the content to the list of content
            transform_result.transform_result_content.append(
                transform_result_content
            )
            # add the result to the list of result
            results_transform.append(transform_result)
        return results_transform

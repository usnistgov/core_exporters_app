""" Blob exporter
"""
from core_exporters_app.exporters.exporter import AbstractExporter, TransformResult, TransformResultContent
import re
import urllib2


class BlobExporter(AbstractExporter):
    """ BLOB Exporter. Allows to find and download all blobs from an xml content
    """
    def __init__(self):
        self.name = "BLOB"
        self.extension = ".blob"

    def transform(self, xml_inputs):
        """ find and download all blobs from an xml content

        Args:
            xml_inputs:

        Returns:

        """
        results_transform = []
        for xml_item in xml_inputs:
            # get the sha of the xml
            sha = AbstractExporter.get_sha(xml_item['xml_content'])
            # get the name of the xml document representing the source document name
            document_name_with_sha = AbstractExporter.get_title_document(xml_item['title'], xml_item['xml_content'])
            transform_result = TransformResult()
            transform_result.source_document_name = document_name_with_sha

            # Get all url from xml content
            urls = _get_blob_url_list_from_xml(xml_item['xml_content'])

            # Get all blobs from urls
            for url in urls:
                try:
                    # Download the blob from the url
                    blob_file = urllib2.urlopen(url)
                    blob_file_read = blob_file.read()
                    # generates the file name
                    blob_name = _get_filename_from_blob(blob_file.info(), blob_file_read, sha)
                    # generates an content result representing the blob file
                    transform_result_content = TransformResultContent()
                    transform_result_content.file_name = blob_name
                    transform_result_content.content_converted = blob_file_read
                    # Don't need any additional extension, Is generated with the file name
                    transform_result_content.content_extension = ""
                    # add the blob to the result list
                    transform_result.transform_result_content.append(transform_result_content)
                except Exception:
                    pass

            results_transform.append(transform_result)
        return results_transform


def _get_blob_url_list_from_xml(xml):
    """ Returns all blob's url list

    Args:
        xml:

    Returns:

    """
    return re.findall('>(http[s]?:.+/rest/blob\?id=[^<]+)', xml)


def _get_filename_from_blob(blob_file_info, blob_file_read, sha_from_xml):
    """ Returns the file name like "file_name.sha3.extension"

    Args:
        blob_file_info:
        blob_file_read:
        sha_from_xml:

    Returns:

    """
    raw = next((raw for raw in blob_file_info.headers if 'filename' in raw), None)
    sha = AbstractExporter.get_sha(blob_file_read)
    if raw is not None:
        # generates the file name
        file_names = re.findall("filename=(.+)", raw)
        if len(file_names) > 0:
            file_name = file_names[0]
            # split by all dotes
            file_name_split = file_name.split('.')
            # file name start with the first element
            return_value = file_name_split[0]
            # loop on the list and generate the file name
            for index in xrange(1, len(file_name_split)):
                # If is the last element, we insert the sha before the extension
                if index == len(file_name_split) - 1:
                    return_value += '.' + sha_from_xml + '.' + sha
                return_value += '.' + file_name_split[index]
            # file_name.sha.extension
            return return_value.replace('\r', '')
    else:
        # if header have no filename, we return the sha only
        return sha

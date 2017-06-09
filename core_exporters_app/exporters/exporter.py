""" Abstract class exporter
"""
from core_exporters_app.components.exported_compressed_file.models import ExportedCompressedFile
from cStringIO import StringIO
from abc import ABCMeta, abstractmethod
import core_exporters_app.components.exported_compressed_file.api as exported_compressed_file_api
import os
import hashlib
import sha3
import importlib
import zipfile


class AbstractExporter(object):
    """
    Export data to different formats
        - export: export the data
        - transform: transforms a XML to another format
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        self.exporter_name = ""
        self.exporter_extension = ""

    @abstractmethod
    def transform(self, results):
        """
            Method: Returns converted data
        """
        raise NotImplementedError("This method is not implemented.")

    @staticmethod
    def export(transformed_result_list):
        """
            Method: Exports the data
        """
        # Creation of the compressed file with is_ready to false
        exported_file = ExportedCompressedFile(file_name='Query_Results.zip',
                                               is_ready=False,
                                               mime_type="application/zip")

        # Save in database to generate an Id and be accessible via url
        exported_compressed_file_api.upsert(exported_file)

        # Generate the zip file
        AbstractExporter.generate_zip(exported_file, transformed_result_list)

        # Returns the id generated
        return exported_file.id

    @staticmethod
    def get_title_document(document_name, content):
        """ Add a Sha-3 and returns the title of the document exported

        Args:
            document_name:
            content:

        Returns:

        """
        # generate sha
        sha = AbstractExporter.get_sha(content)
        # delete the extension of the document name
        document_name = os.path.splitext(document_name)[0]
        return "{!s}.{!s}".format(document_name, sha)

    @staticmethod
    def get_sha(content, number_of_characters=8):
        """ Generates the Sha-3 from the xml content

        Args:
            content:
            number_of_characters:

        Returns:

        """
        # TODO: Could be moved to an util
        if number_of_characters < 0 or number_of_characters > 128:
            raise Exception("number_of_characters should be > 0 and < 128")

        # new instance of sha3
        hash_result = hashlib.sha3_512()
        # if unicode, the content must be encoded
        if isinstance(content, unicode):
            content = content.encode('utf-8')
        hash_result.update(content)
        # take first 8 letters
        return hash_result.hexdigest()[0:number_of_characters]

    @staticmethod
    def generate_zip(exported_compressed_file, transformed_result_list):
        """ Generates the zip file

        Args:
            exported_compressed_file:
            transformed_result_list:

        Returns:

        """
        # Needed otherwise the file in db is not updated
        exported_compressed_file = exported_compressed_file_api.get_by_id(exported_compressed_file.id)

        # ZIP fileCreation
        in_memory = StringIO()
        zip = zipfile.ZipFile(in_memory, "a")

        # For each result
        for transformed_result in transformed_result_list:
            # Loops on converted file
            for result in transformed_result:
                # Loops on contents converted for each file
                for content in result.transform_result_content:
                    path = "{!s}/{!s}{!s}".format(result.source_document_name,
                                                  content.file_name,
                                                  content.content_extension)
                    zip.writestr(path, content.content_converted)

        # fix for Linux zip files read in Windows
        for xmlFile in zip.filelist:
            xmlFile.create_system = 0

        # Close zip file
        zip.close()

        # ZIP file to be downloaded
        in_memory.seek(0)

        # save the file and upset the object
        exported_compressed_file.file.put(in_memory, content_type=exported_compressed_file.mime_type)
        exported_compressed_file.is_ready = True
        exported_compressed_file_api.upsert(exported_compressed_file)


class TransformResult(object):
    """ Represents a result after transformation
    """
    def __init__(self):
        """
            source_document_name:
                It will be the source document name like "myFile.xml"
            transform_result_content:
                List of result.
                One result expected for simple conversion like XML, Json
                but zero or N result for blob export
        """
        self.source_document_name = ""
        self.transform_result_content = []


class TransformResultContent(object):
    """ Represents a result content
    """

    def __init__(self):
        """
            file_name:
                For simple conversion like XML, JSON etc.. The file name
                will be the same as the TransformResult without extension
                For conversion like Blob, the file name will be the blob's
                file name
            content_converted:
                The content converter in string (XML, Json, unicode)
            content_extension:
                .xml, .json, .png
        """
        self.file_name = ""
        self.content_converted = ""
        self.content_extension = ""


def get_exporter_module_from_url(exporter_url):
    """ Returns the exporter module from exporter url

    Args:
        exporter_url:

    Returns:

    """
    pkglist = exporter_url.split('.')

    pkgs = '.'.join(pkglist[:-1])
    func = pkglist[-1:][0]

    imported_pkgs = importlib.import_module(pkgs)
    a = getattr(imported_pkgs, func)
    module = a()

    return module


def generate_zip_wrapper(args):
    """ wraps generate zip parameter

    Args:
        args:

    Returns:

    """
    return AbstractExporter.generate_zip(*args)

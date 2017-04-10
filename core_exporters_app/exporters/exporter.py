""" Abstract class exporter
"""
from abc import ABCMeta, abstractmethod


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
    def export(self):
        """
            Method: Exports the data
        """
        raise NotImplementedError("This method is not implemented.")

    @abstractmethod
    def transform(self, results):
        """
            Method: Returns converted data
        """
        raise NotImplementedError("This method is not implemented.")


class TransformResult(object):
    """
        Represents a result after transformation
    """
    def __init__(self):
        self.source_document_name = ""
        self.content = []


class ResultContent(object):
    """
    Represents a result content
    """

    def __init__(self):
        self.file_name = ""
        self.file_content = ""
        self.extension = ""

""" XML exporter
"""
from core_exporters_app.exporters.exporter import AbstractExporter


class XmlExporter(AbstractExporter):
    """ XML Exporter. Allows to transform an XML to a JSON file
    """
    def __init__(self):
        self.name = "XML"
        self.extension = ".xml"

    def transform(self, results):
        """ Transforms the input to a json content

        Args:
            results:

        Returns:

        """
        pass

    def export(self):
        """ Returns the converted data

        Returns:

        """
        pass





""" Json exporter
"""
from core_exporters_app.exporters.exporter import AbstractExporter


class JsonExporter(AbstractExporter):
    """ JSON Exporter. Allows to transform an XML to a JSON
    """
    def __init__(self):
        self.name = "JSON"
        self.extension = ".json"

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





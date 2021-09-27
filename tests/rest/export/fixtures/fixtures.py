""" Fixture files for Exporters
"""
import core_exporters_app.commons.constants as constants
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_exporters_app.components.exporter.models import Exporter
from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface


class ExportDataFixtures(FixtureInterface):
    """Exporter fixtures"""

    data_1 = None
    template = None
    exporter_xml = None
    exporter_json = None
    exporter_xsl = None
    data_collection = None

    def insert_data(self):
        """Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_data_collection()

    def generate_data_collection(self):
        """Generate a Data collection.

        Returns:

        """

        self.generate_template()

        self.data_1 = Data()

        self.exporter_xml = Exporter(
            name="XML",
            url=constants.XML_URL,
            enable_by_default=True,
            templates=[self.template],
        ).save()

        self.exporter_json = Exporter(
            name="JSON",
            url=constants.JSON_URL,
            enable_by_default=True,
            templates=[self.template],
        ).save()

        self.exporter_xsl = Exporter(
            name="XSL_trans",
            url=constants.XSL_URL,
            enable_by_default=True,
            templates=[self.template],
        ).save()

        self.data_collection = [
            self.data_1,
            self.exporter_xml,
            self.exporter_json,
            self.exporter_xsl,
        ]

    def generate_template(self):
        """Generate an unique Template.

        Returns:

        """
        template = Template()

        xsd = (
            '<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">'
            ' <xsd:element name="root" type="hamza"/>'
            '     <xsd:complexType name="hamza">'
            "         <xsd:sequence>  "
            '             <xsd:element name="string" type="xsd:string"/>'
            "         </xsd:sequence>"
            "     </xsd:complexType>"
            "</xsd:schema>"
        )

        template.content = xsd
        template.hash = ""
        template.filename = "filename"
        self.template = template.save()

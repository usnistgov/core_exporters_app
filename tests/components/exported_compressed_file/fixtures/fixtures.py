""" Fixture files for Exporters
"""

from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)
from core_exporters_app.components.exported_compressed_file.models import (
    ExportedCompressedFile,
)


class ExportedCompressedFileFixtures(FixtureInterface):
    """Exporter fixtures"""

    exported_compressed_file_1 = None
    exported_compressed_file_2 = None
    exported_compressed_file_3 = None
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
        self.exported_compressed_file_1 = ExportedCompressedFile(
            file_name="exported_compressed_file_1",
            mime_type="application/zip",
            is_ready=True,
            user_id="1",
        )
        self.exported_compressed_file_1.save()

        self.exported_compressed_file_2 = ExportedCompressedFile(
            file_name="exported_compressed_file_2",
            mime_type="application/zip",
            is_ready=True,
            user_id="2",
        )
        self.exported_compressed_file_2.save()

        self.exported_compressed_file_3 = ExportedCompressedFile(
            file_name="exported_compressed_file_3",
            mime_type="application/zip",
            is_ready=True,
            user_id="None",
        )
        self.exported_compressed_file_3.save()

        self.data_collection = [
            self.exported_compressed_file_1,
            self.exported_compressed_file_2,
            self.exported_compressed_file_3,
        ]

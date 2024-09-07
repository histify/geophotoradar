import time
from csv import DictReader
from operator import itemgetter

from app.importer import Importer
from app.settings import settings
from tests.case import TestCase


class TestElastic(TestCase):
    def test_index_exists(self):
        self.assertTrue(self.elastic.connection.indices.exists(index=settings.elastic_index))

    def test_index_and_query_document(self):
        self.assertEqual([], self.elastic.search_documents(11.5751872644, 48.1285358227, "1km"))
        self.elastic.index(
            {
                "title": "Fraunhofer Apotheke",
                "image_url": "https://zentralgut.ch/content/BibZug_TD_23_01705/800/0/TD_23_01705.jpg",
                "id": "BibZug_TD_23_01705",
                "coordinates": {"type": "Point", "coordinates": [11.5751872644, 48.1285358227]},
                "zentralgut_url": "https://n2t.net/ark:/63274/bz1f17g",
                "iiif_url": "https://zentralgut.ch/api/v1/records/BibZug_TD_23_01705/files/images/TD_23_01705.jpg",
            },
        )
        self.assertEqual(
            ["Fraunhofer Apotheke"],
            list(map(itemgetter("title"), self.elastic.search_documents(11.5751872644, 48.1285358227, "1km"))),
        )

    def test_import_records(self):
        importer = Importer()
        with self.asset("test.csv").open("r") as fio:
            records = importer.read_csv_to_records(DictReader(fio))

        self.elastic.import_records(records)
        time.sleep(1)
        self.assertEqual(self.elastic.connection.count(index=settings.elastic_index)["count"], 7)

from csv import DictReader
from operator import itemgetter

from app.importer import Importer
from tests.case import TestCase


class TestImporter(TestCase):
    def test_read_csv_to_records(self):
        importer = Importer()
        with self.asset("test.csv").open("r") as fio:
            records = importer.read_csv_to_records(DictReader(fio))

        self.assertEqual(len(records), 7)
        self.assertEqual(records[0].lat, 47.18604132321729)

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

import time
from csv import DictReader
from io import StringIO
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

        csv_data = """title,id,coordinates,source_system_url,image_url,iiif_url
NOB kurzer Güterzug am Nordende Bahnhof Zug mit 3 Bahnangestellten,BibZug_TD_23_00002,"47.18604132321729, 8.517235125628236",ark:/63274/bz1b161,https://zentralgut.ch/content/BibZug_TD_23_00002/800/0/TD_23_00002.jpg,https://zentralgut.ch/api/v1/records/BibZug_TD_23_00002/files/images/TD_23_00002.jpg
Karl Muther Junior auf einer Parkbank mit Zigarette,BibZug_TD_23_00003,,ark:/63274/bz16b3t,https://zentralgut.ch/content/BibZug_TD_23_00003/800/0/TD_23_00003.jpg,https://zentralgut.ch/api/v1/records/BibZug_TD_23_00003/files/images/TD_23_00003.jpg
Prozession mit Soldaten,BibZug_TD_23_00009,,ark:/63274/bz1dt88,https://zentralgut.ch/content/BibZug_TD_23_00009/800/0/TD_23_00009.jpg,https://zentralgut.ch/api/v1/records/BibZug_TD_23_00009/files/images/TD_23_00009.jpg
Prozession mit Soldaten,BibZug_TD_23_00010,,ark:/63274/bz19173,https://zentralgut.ch/content/BibZug_TD_23_00010/800/0/TD_23_00010.jpg,https://zentralgut.ch/api/v1/records/BibZug_TD_23_00010/files/images/TD_23_00010.jpg
Ruelle des Maçons in Fribourg,BibZug_TD_23_00011,,ark:/63274/bz15b22,https://zentralgut.ch/content/BibZug_TD_23_00011/800/0/TD_23_00011.jpg,https://zentralgut.ch/api/v1/records/BibZug_TD_23_00011/files/images/TD_23_00011.jpg
Eingang des Hotel Continental,BibZug_TD_23_00012,,ark:/63274/bz11j04,https://zentralgut.ch/content/BibZug_TD_23_00012/800/0/TD_23_00012.jpg,https://zentralgut.ch/api/v1/records/BibZug_TD_23_00012/files/images/TD_23_00012.jpg
Bau eines Torbogens; Standort unbekannt,BibZug_TD_23_00018,,ark:/63274/bz18452,https://zentralgut.ch/content/BibZug_TD_23_00018/800/0/TD_23_00018.jpg,https://zentralgut.ch/api/v1/records/BibZug_TD_23_00018/files/images/TD_23_00018.jpg
Bergsteiger auf einem Gipfel,BibZug_TD_23_00080,,ark:/63274/bz1wj15,https://zentralgut.ch/content/BibZug_TD_23_00080/800/0/TD_23_00080.jpg,https://zentralgut.ch/api/v1/records/BibZug_TD_23_00080/files/images/TD_23_00080.jpg
Eine Familie vor einem leicht verschneiten Berghang,BibZug_TD_23_00081,,ark:/63274/bz1rt79,https://zentralgut.ch/content/BibZug_TD_23_00081/800/0/TD_23_00081.jpg,https://zentralgut.ch/api/v1/records/BibZug_TD_23_00081/files/images/TD_23_00081.jpg
Das Schnetztor,BibZug_TD_23_02055,"47.6587169526, 9.17097352869",ark:/63274/bz1s472,https://zentralgut.ch/content/BibZug_TD_23_02055/800/0/TD_23_02055.jpg,https://zentralgut.ch/api/v1/records/BibZug_TD_23_02055/files/images/TD_23_02055.jpg
Das Schnetztor in Konstanz,BibZug_TD_23_02056,"47.6587169526, 9.17097352869",ark:/63274/bz1nf4v,https://zentralgut.ch/content/BibZug_TD_23_02056/800/0/TD_23_02056.jpg,https://zentralgut.ch/api/v1/records/BibZug_TD_23_02056/files/images/TD_23_02056.jpg
Das Schnetztor der historischen Stadtmauer in Konstanz,BibZug_TD_23_02057,"47.6587169526, 9.17097352869",ark:/63274/bz1hr07,https://zentralgut.ch/content/BibZug_TD_23_02057/800/0/TD_23_02057.jpg,https://zentralgut.ch/api/v1/records/BibZug_TD_23_02057/files/images/TD_23_02057.jpg
Eine Gruppe des S.A.C.,BibZug_TD_23_03210,"46.7744589937, 8.26801519264",ark:/63274/bz1hf4g,https://zentralgut.ch/content/BibZug_TD_23_03210/800/0/TD_23_03210.jpg,https://zentralgut.ch/api/v1/records/BibZug_TD_23_03210/files/images/TD_23_03210.jpg
Portrait von drei Personen,BibZug_TD_23_03211,"46.7744589937, 8.26801519264",ark:/63274/bz1cn14,https://zentralgut.ch/content/BibZug_TD_23_03211/800/0/TD_23_03211.jpg,https://zentralgut.ch/api/v1/records/BibZug_TD_23_03211/files/images/TD_23_03211.jpg
Eine Gruppe Wanderer,BibZug_TD_23_03215,"46.7744589937, 8.26801519264",ark:/63274/bz17x8p,https://zentralgut.ch/content/BibZug_TD_23_03215/800/0/TD_23_03215.jpg,https://zentralgut.ch/api/v1/records/BibZug_TD_23_03215/files/images/TD_23_03215.jpg
Blick über ein Tal,BibZug_TD_23_03350,,ark:/63274/bz1gf5j,https://zentralgut.ch/content/BibZug_TD_23_03350/800/0/TD_23_03350.jpg,https://zentralgut.ch/api/v1/records/BibZug_TD_23_03350/files/images/TD_23_03350.jpg
"""

        csv_file = StringIO(csv_data)
        csv_reader = DictReader(csv_file)

        records = importer.read_csv_to_records(csv_reader)
        self.elastic.import_records(records)
        time.sleep(1)
        self.assertEqual(self.elastic.connection.count(index=settings.elastic_index)["count"], 7)

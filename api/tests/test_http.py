from io import BytesIO
from pathlib import Path
from tempfile import NamedTemporaryFile

from app.settings import settings
from tests.case import TestCase


class TestHTTP(TestCase):
    def test_root_redirects_to_docs(self):
        response = self.client.get("/api", follow_redirects=False)
        self.assertEqual(response.status_code, 307)
        self.assertEqual("/api/docs", response.headers.get("location"))

    def test_health(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual({"status": "ok"}, response.json())

    def test_photos_querying(self):
        rathausquai = {
            "title": "Der Überschwemmte Rathausquai der Stadt Luzern",
            "image_url": "https://zentralgut.ch/content/BibZug_TD_23_01990/800/0/TD_23_01990.jpg",
            "id": "BibZug_TD_23_01990",
            "coordinates": {"type": "Point", "coordinates": [8.30707289986, 47.0519806883]},
            "zentralgut_url": "https://n2t.net/ark:/63274/bz1rb4r",
            "iiif_url": "https://zentralgut.ch/api/v1/records/BibZug_TD_23_01990/files/images/TD_23_01990.jpg",
        }
        seeblick = {
            "title": "Villa Seeblick",
            "image_url": "https://zentralgut.ch/content/BibZug_TD_23_02548/800/0/TD_23_02548.jpg",
            "id": "BibZug_TD_23_02548",
            "coordinates": {"type": "Point", "coordinates": [8.513045174201151, 47.16136672113505]},
            "zentralgut_url": "https://n2t.net/ark:/63274/bz1s18b",
            "iiif_url": "https://zentralgut.ch/api/v1/records/BibZug_TD_23_02548/files/images/TD_23_02548.jpg",
        }
        self.elastic.index(rathausquai)
        self.elastic.index(seeblick)

        response = self.client.get(
            "/api/photos",
            params={
                "longitude": 8.513045174201151,
                "latitude": 47.16136672113505,
                "radius": 1000000,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assert_json_equal([rathausquai, seeblick], response.json())

        response = self.client.get(
            "/api/photos",
            params={
                "longitude": 8.513045174201151,
                "latitude": 47.16136672113505,
                "radius": 10,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assert_json_equal([seeblick], response.json())

    def test_data_import_endpoint_is_protected(self):
        response = self.client.post(
            "/api/import/",
            files={"file": ("foo.csv", BytesIO(), "text/csv")},
        )
        self.assertEqual(403, response.status_code)
        self.assertEqual({"detail": "Not authenticated"}, response.json())

    def test_data_import(self):
        with NamedTemporaryFile(suffix=".csv") as fio:
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
            fio.write(csv_data.encode('utf-8'))
            fio.flush()
            fio.seek(0)
            response = self.client.post(
                "/api/import/",
                files={"file": (Path(fio.name).name, fio, "text/csv")},
                headers={"Authorization": f"Bearer {settings.api_import_token}"},
            )
            self.assertEqual(200, response.status_code, response.content)
            expected_result = {'message': 'Finished: 7 documents indexed, 0 failed.', 'status': 'ok'}
            self.assertEqual(expected_result, response.json())

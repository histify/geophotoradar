from io import BytesIO
from pathlib import Path

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
        self.assert_json_equal([seeblick, rathausquai], response.json())

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
        with self.asset("test.csv").open("rb") as fio:
            response = self.client.post(
                "/api/import/",
                files={"file": (Path(fio.name).name, fio, "text/csv")},
                headers={"Authorization": f"Bearer {settings.api_import_token}"},
            )
            self.assertEqual(200, response.status_code, response.content)
            expected_result = {"message": "Finished: 7 documents indexed, 0 failed.", "status": "ok"}
            self.assertEqual(expected_result, response.json())

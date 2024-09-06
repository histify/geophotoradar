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
                "latitude": 47.16136672113505,
                "longitude": 8.513045174201151,
                "radius": 1000000,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assert_json_equal([rathausquai, seeblick], response.json())

        response = self.client.get(
            "/api/photos",
            params={
                "latitude": 47.16136672113505,
                "longitude": 8.513045174201151,
                "radius": 10,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assert_json_equal([seeblick], response.json())

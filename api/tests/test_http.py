from tests.case import TestCase


class TestHealthEndpoint(TestCase):

    def test_health(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual({"status": "ok"}, response.json())

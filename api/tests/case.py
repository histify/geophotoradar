import json
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.elastic import Elastic
from app.server import app


class TestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.client = TestClient(app)
        self.elastic = Elastic()
        self.elastic.delete_index()
        self.elastic.create_index()
        self.assets = Path(__file__).parent / "assets"

    def assert_json_equal(self, expected, got, msg=None):
        got = json.dumps(got, sort_keys=True, indent=4)
        expected = json.dumps(expected, sort_keys=True, indent=4)
        self.maxDiff = None
        self.assertMultiLineEqual(expected, got, msg)

    def asset(self, filename: str) -> Path:
        return self.assets / filename

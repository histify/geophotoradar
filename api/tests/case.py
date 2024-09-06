import unittest

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

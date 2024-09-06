import unittest

from fastapi.testclient import TestClient

from app.server import app


class TestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.client = TestClient(app)

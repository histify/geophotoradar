from app.settings import settings
from tests.case import TestCase


class TestElastic(TestCase):

    def test_index_exists(self):
        self.assertTrue(self.elastic.connection.indices.exists(index=settings.elastic_index))

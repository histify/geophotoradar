from operator import itemgetter

from elastic_transport import ObjectApiResponse
from elasticsearch import Elasticsearch

from app.settings import settings


class Elastic:
    """The `Elastic` class has the purpose to abstract the elasticsearch
    API. For instance, it abstracts the index used within elasticsearch.
    """

    def __init__(self) -> None:
        self.index_name = settings.elastic_index
        self.connection = Elasticsearch(
            [settings.elastic_url],
            basic_auth=(settings.elastic_user, settings.elastic_password),
        )

    def search_documents(self, longitude: float, latitude: float, radius: str) -> list[dict]:
        """Search for documents in the index, returning only a list of documents as dicts"""
        response = self.search(
            {
                "bool": {
                    "must": {"match_all": {}},
                    "filter": {"geo_distance": {"distance": radius, "coordinates": {"lon": longitude, "lat": latitude}}},
                }
            }
        )
        hits = response["hits"]["hits"]
        return list(map(itemgetter("_source"), hits))

    def search(self, query: dict) -> ObjectApiResponse:
        """Search for documents in the index, returning the elastic search response."""
        return self.connection.search(index=self.index_name, query=query)

    def index(self, document: dict) -> None:
        """Add a document to the elasticsearch index."""
        self.connection.index(index=self.index_name, document=document, refresh="wait_for")

    def delete_index(self) -> None:
        """Delete the whole elasticsearch  index."""
        if self.connection.indices.exists(index=self.index_name):
            self.connection.indices.delete(index=self.index_name)

    def create_index(self) -> None:
        """Create a new elasticsearch index."""
        if not self.connection.indices.exists(index=self.index_name):
            self.connection.indices.create(
                index=self.index_name,
                body={
                    "mappings": {
                        "properties": {"coordinates": {"type": "geo_point"}},
                    }
                },
            )

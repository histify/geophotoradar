from elasticsearch import Elasticsearch

from app.settings import settings


class Elastic:
    def __init__(self) -> None:
        self.connection = Elasticsearch(
            [settings.elastic_url],
            basic_auth=(settings.elastic_user, settings.elastic_password),
        )

    def delete_index(self) -> None:
        """Delete the whole elasticsearch  index."""
        if self.connection.indices.exists(index=settings.elastic_index):
            self.connection.indices.delete(index=settings.elastic_index)

    def create_index(self) -> None:
        """Create a new elasticsearch index."""
        if not self.connection.indices.exists(index=settings.elastic_index):
            self.connection.indices.create(
                index=settings.elastic_index,
                body={
                    "mappings": {
                        "properties": {"coordinates": {"type": "geo_point"}},
                    }
                },
            )

    def index(self, document: dict) -> None:
        """Add a document to the elasticsearch index."""
        self.connection.index(
            index=settings.elastic_index,
            document=document,
            refresh="wait_for",
        )

    def search(self, query: dict) -> None:
        """Search for documents in the index."""
        return self.connection.search(index=settings.elastic_index, query=query)

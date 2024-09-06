from elasticsearch import Elasticsearch

from app.settings import settings


class Elastic:
    def __init__(self) -> None:
        self.connection = Elasticsearch(
            [settings.elastic_url],
            basic_auth=(settings.elastic_user, settings.elastic_password),
        )

    def delete_index(self) -> None:
        if self.connection.indices.exists(index=settings.elastic_index):
            self.connection.indices.delete(index=settings.elastic_index)

    def create_index(self) -> None:
        if not self.connection.indices.exists(index=settings.elastic_index):
            self.connection.indices.create(index=settings.elastic_index)

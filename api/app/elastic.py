from operator import itemgetter
from typing import List

from elastic_transport import ObjectApiResponse
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

from app.record import Record
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
                "size": 1000,
                "query": {
                    "bool": {
                        "must": {"match_all": {}},
                        "filter": {"geo_distance": {"distance": radius, "coordinates": {"lat": latitude, "lon": longitude}}},
                    }
                },
                "sort": [
                    {
                        "_geo_distance": {
                            "coordinates": {"lat": latitude, "lon": longitude},
                            "order": "asc",
                            "unit": "km",
                            "mode": "min",
                            "distance_type": "arc",
                            "ignore_unmapped": True,
                        }
                    }
                ],
                "script_fields": {"distance_in_m": {"script": f"doc['coordinates'].arcDistance({latitude}, {longitude})"}},
                "_source": ["*"],
            }
        )
        hits = response["hits"]["hits"]

        source_fields = list(map(itemgetter("_source"), hits))
        scripted_fields = list(map(itemgetter("fields"), hits))

        return list(map(lambda thing: {**thing.get("_source"), "distance": thing.get("fields")["distance_in_m"][0]}, hits))

    def search(self, query: dict) -> ObjectApiResponse:
        """Search for documents in the index, returning the elastic search response."""
        return self.connection.search(index=self.index_name, body=query)

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

    def import_records(self, records: List[Record]) -> str:
        self.create_index()
        success, failed = 0, 0
        for ok, action in streaming_bulk(
            client=self.connection,
            index=self.index_name,
            actions=self.generate_actions(records),
        ):
            if ok:
                success += 1
            else:
                failed += 1
        return f"Finished: {success} documents indexed, {failed} failed."

    def generate_actions(self, records: List[Record]):
        """This function is passed into the bulk()
        helper to create many documents in sequence.
        """
        for record in records:
            doc = record.record_to_dict()
            yield doc

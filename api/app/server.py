from operator import itemgetter

from fastapi import FastAPI
from fastapi import Query
from fastapi import Request

from app.elastic import Elastic
from app.settings import settings


app = FastAPI(debug=settings.fastapi_debug)


@app.get("/api/health")
async def health(request: Request):
    return {"status": "ok"}


@app.get("/api/photos")
async def photos(latitude: float = Query(...), longitude: float = Query(...), radius: float = Query(...)):
    query = {
        "bool": {
            "must": {"match_all": {}},
            "filter": {"geo_distance": {"distance": f"{radius}m", "coordinates": {"lat": latitude, "lon": longitude}}},
        }
    }
    response = Elastic().search(query=query)
    hits = response["hits"]["hits"]
    documents = list(map(itemgetter("_source"), hits))
    return documents

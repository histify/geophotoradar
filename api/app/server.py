from operator import itemgetter

from fastapi import FastAPI
from fastapi import Query
from fastapi.responses import RedirectResponse

from app.elastic import Elastic
from app.settings import settings


app = FastAPI(
    debug=settings.fastapi_debug,
    title="GeoPhotoRadar API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)


@app.get("/api", include_in_schema=False)
async def root():
    return RedirectResponse("/api/docs")


@app.get("/api/health")
async def health():
    """The health endpoint is used for health checks, indicating whether
    the API is running."""
    return {"status": "ok"}


@app.get("/api/photos")
async def photos(latitude: float = Query(...), longitude: float = Query(...), radius: float = Query(...)):
    """The photos endpoint queries the database for fotos in a specific radious of a location."""
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

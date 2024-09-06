from fastapi import FastAPI
from fastapi import File
from fastapi import Query
from fastapi import UploadFile
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
async def photos(longitude: float = Query(...), latitude: float = Query(...), radius: float = Query(...)):
    """The photos endpoint queries the database for fotos in a specific radious of a location."""
    return Elastic().search_documents(longitude=longitude, latitude=latitude, radius=f"{radius}m")


@app.post("/api/import")
async def import_data(file: UploadFile = File(...)):
    return file.filename

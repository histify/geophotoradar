import csv
from io import StringIO

from fastapi import Depends
from fastapi import FastAPI
from fastapi import File
from fastapi import HTTPException
from fastapi import Query
from fastapi import status
from fastapi import UploadFile
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from app.elastic import Elastic
from app.importer import Importer
from app.settings import settings


app = FastAPI(
    debug=settings.fastapi_debug,
    title="GeoPhotoRadar API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    if credentials.credentials != settings.api_import_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"}
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
async def import_data(file: UploadFile = File(...), token: HTTPAuthorizationCredentials = Depends(verify_token)):
    content = await file.read()

    # Decode the content and use StringIO to emulate a file-like object
    csv_content = content.decode("utf-8")
    csv_reader = csv.DictReader(StringIO(csv_content))

    importer = Importer()
    records = importer.read_csv_to_records(csv_reader)
    message = Elastic().import_records(records)
    return {
        "status": "ok",
        "message": message,
    }

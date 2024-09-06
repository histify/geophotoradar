from fastapi import FastAPI
from fastapi import Request

from app.settings import settings


app = FastAPI(debug=settings.fastapi_debug)


@app.get("/api/health")
async def health(request: Request):
    return {"status": "ok"}

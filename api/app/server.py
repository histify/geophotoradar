from fastapi import FastAPI

from app.routers import root
from app.settings import settings


app = FastAPI(debug=settings.fastapi_debug)
app.include_router(root.router)

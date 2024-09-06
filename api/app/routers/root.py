from fastapi import APIRouter
from fastapi import Request


router = APIRouter()


@router.get("/health")
async def health(request: Request):
    return {"status": "ok"}

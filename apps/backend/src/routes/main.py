"""
Routes for the main API.
"""

from fastapi import APIRouter

from src.routes.v1.main import router as v1_router

router = APIRouter()


@router.get("/healthz")
async def health():
    return {"status": "ok"}


@router.get("/")
async def hello():
    return {"message": "Hello, World!"}

router.include_router(v1_router)

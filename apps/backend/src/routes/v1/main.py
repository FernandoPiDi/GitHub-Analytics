"""
Routes for the v1 of the API.
"""

from fastapi import APIRouter

from src.routes.v1.analytics import router as analytics_router

router = APIRouter(prefix="/v1")

router.include_router(analytics_router)

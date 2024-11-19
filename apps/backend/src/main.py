"""Main entry point for the API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.main import router as api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
from fastapi import APIRouter
from app.api.routes import document, extract

api_router = APIRouter()

api_router.include_router(document.router, prefix="/documents", tags=["Documents"])
api_router.include_router(extract.router, prefix="/extract", tags=["Extract"])
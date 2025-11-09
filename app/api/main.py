from fastapi import APIRouter

from app.api.routes import extract
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(extract.router)

api_router.prefix = settings.API_V1_STR
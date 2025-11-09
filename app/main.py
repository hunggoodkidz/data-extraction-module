from fastapi import FastAPI
from app.api.main import api_router
from app.core.config import settings
from app.core.database import create_db_and_tables

app = FastAPI(title="Data Extraction API")

@app.on_event("startup")
def startup():
    create_db_and_tables()

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "API is running", "docs": settings.API_V1_STR + "/docs"}
from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# PostgreSQL engine connection
engine = create_engine(settings.DATABASE_URL, echo=True)

def create_db_and_tables():
    """
    Import all SQLModel models here to register them with metadata,
    then create tables in PostgreSQL if they don't exist.
    """
    from app.models import company, fund, investment, financial, document, extracted_field, correction
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
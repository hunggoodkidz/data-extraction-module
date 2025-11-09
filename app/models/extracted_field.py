from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime

class ExtractedField(SQLModel, table=True):
    __tablename__ = "extracted_field"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    document_id: UUID = Field(foreign_key="document.id")
    field_name: str  # e.g., "transaction_value", "company_name"
    extracted_value: Optional[str] = None

    page_number: Optional[int] = None
    source_text: Optional[str] = None

    confidence_score: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

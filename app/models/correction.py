from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime

class Correction(SQLModel, table=True):
    __tablename__ = "correction"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    extracted_field_id: UUID = Field(foreign_key="extracted_field.id")
    corrected_value: str

    corrected_by_user: Optional[str] = None
    reason: Optional[str] = None

    corrected_at: datetime = Field(default_factory=datetime.utcnow)

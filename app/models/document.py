from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime

class Document(SQLModel, table=True):
    __tablename__ = "document"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    fund_id: Optional[UUID] = Field(default=None, foreign_key="fund.id")
    company_id: Optional[UUID] = Field(default=None, foreign_key="company.id")

    file_name: str
    file_path: str

    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

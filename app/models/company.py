from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID, uuid4

class Company(SQLModel, table=True):
    __tablename__ = "company"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    holding_company: Optional[str] = None
    description: Optional[str] = None
    head_office_location: Optional[str] = None
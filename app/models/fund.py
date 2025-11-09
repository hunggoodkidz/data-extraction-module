from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional

class Fund(SQLModel, table=True):
    __tablename__ = "fund" 
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    type: Optional[str] = None
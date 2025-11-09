from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional
from datetime import date
from decimal import Decimal

class Investment(SQLModel, table=True):
    __tablename__ = "investment"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    
    fund_id: Optional[UUID] = Field(default=None, foreign_key="fund.id")
    company_id: Optional[UUID] = Field(default=None, foreign_key="company.id")

    fund_role: Optional[str] = None
    investment_type: Optional[str] = None  # Primary, Co-investment, etc.
    ownership_percent: Optional[float] = None
    board_members: Optional[str] = None

    date_of_first_completion: Optional[date] = None
    transaction_value: Optional[Decimal] = None
    current_cost: Optional[Decimal] = None
    fair_value: Optional[Decimal] = None

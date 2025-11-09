from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from typing import Optional
from decimal import Decimal

class FinancialHighlight(SQLModel, table=True):
    __tablename__ = "financial_highlight"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    company_id: UUID = Field(foreign_key="company.id")

    period: str  # e.g., "FY2023", "Dec-24"
    currency: Optional[str] = None  # e.g., "KRW bn", "USD mn"

    revenue: Optional[Decimal] = None
    ebitda: Optional[Decimal] = None
    ebitda_margin: Optional[Decimal] = None
    ebit: Optional[Decimal] = None
    ebit_margin: Optional[Decimal] = None
    net_profit_after_tax: Optional[Decimal] = None
    capex: Optional[Decimal] = None
    net_debt: Optional[Decimal] = None

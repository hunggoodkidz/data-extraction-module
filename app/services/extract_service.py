# app/services/extract_service.py

import json
import pdfplumber
from fastapi import HTTPException
from sqlmodel import Session
from datetime import datetime

from app.models.document import Document
from app.models.extracted_field import ExtractedField
from app.models.company import Company
from app.models.investment import Investment
from app.models.financial import FinancialHighlight

from app.services.ollama_service import call_ollama
from app.utils.cleaner import extract_number
from app.utils.json_parser import parse_ai_json
from app.utils.prompt_builder import (
    build_company_prompt,
    build_financial_prompt
)

# ==========================================================
#  1. Basic PDF Text Extraction
# ==========================================================

def extract_text_from_document(document_id: str, session: Session):
    document = session.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    try:
        with pdfplumber.open(document.file_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""

                extracted = ExtractedField(
                    document_id=document.id,
                    field_name="raw_text",
                    extracted_value=text,
                    page_number=page_number,
                    source_text=text,
                    confidence_score=None,
                    created_at=datetime.utcnow()
                )
                session.add(extracted)

            session.commit()
            return len(pdf.pages)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading PDF: {e}")


# ==========================================================
# 2. Company + Investment Extraction (AI)
# ==========================================================

def extract_company_data_ai(document_id: str, session: Session):
    document = session.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    raw_pages = session.query(ExtractedField).filter(
        ExtractedField.document_id == document_id
    ).order_by(ExtractedField.page_number).all()

    if not raw_pages:
        raise HTTPException(status_code=400, detail="Run /extract/pdf first to extract text.")

    full_text = "\n".join([p.extracted_value or "" for p in raw_pages])
    prompt = build_company_prompt(full_text)
    ai_response = call_ollama(prompt)
    print("\n\n=== RAW AI RESPONSE ===\n", ai_response, "\n=======================\n")

    data = parse_ai_json(ai_response)

    company = Company(
        name=data.get("company_name"),
        holding_company=data.get("holding_company"),
        description=data.get("business_description"),
        head_office_location=data.get("head_office_location")
    )
    session.add(company)
    session.commit()
    session.refresh(company)

    fund_id = document.fund_id

    investment = Investment(
        company_id=company.id,
        fund_id=fund_id,
        fund_role=data.get("fund_role"),
        investment_type=data.get("investment_type"),
        ownership_percent=extract_number(data.get("ownership_percent")),
        date_of_first_completion=data.get("first_completion_date"),
        transaction_value=extract_number(data.get("transaction_value")),
        current_cost=extract_number(data.get("current_cost")),
        fair_value=extract_number(data.get("fair_value"))
    )
    session.add(investment)
    session.commit()
    session.refresh(investment)

    # Link document to company
    document.company_id = company.id
    session.add(document)
    session.commit()

    return {
        "message": "AI extraction completed",
        "company": company,
        "investment": investment,
        "ai_raw_output": data
    }


# ==========================================================
# 3. Financial Highlights Extraction (AI)
# ==========================================================

def extract_financials_ai(document_id: str, session: Session):
    """Extracts numeric financial performance metrics from annual report."""
    document = session.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    raw_pages = session.query(ExtractedField).filter(
        ExtractedField.document_id == document_id
    ).order_by(ExtractedField.page_number).all()

    if not raw_pages:
        raise HTTPException(status_code=400, detail="Run /extract/pdf first to extract text first.")

    full_text = "\n".join([p.extracted_value or "" for p in raw_pages])
    prompt = build_financial_prompt(full_text)
    ai_response = call_ollama(prompt)
    print("\n\n=== AI RAW FINANCIAL RESPONSE ===\n", ai_response, "\n=======================\n")

    try:
        data = parse_ai_json(ai_response)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="AI returned invalid JSON.")

    financial = FinancialHighlight(
        company_id=document.company_id,
        period=data.get("period"),
        currency=data.get("currency"),
        revenue=extract_number(data.get("revenue")),
        ebitda=extract_number(data.get("ebitda")),
        ebitda_margin=extract_number(data.get("ebitda_margin")),
        ebit=extract_number(data.get("ebit")),
        ebit_margin=extract_number(data.get("ebit_margin")),
        net_profit_after_tax=extract_number(data.get("net_profit_after_tax")),
        capex=extract_number(data.get("capex")),
        net_debt=extract_number(data.get("net_debt"))
    )

    session.add(financial)
    session.commit()
    session.refresh(financial)

    return {
        "message": "Financial highlights extracted successfully",
        "financial_highlight": financial,
        "ai_raw_output": data
    }

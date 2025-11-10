from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.services.extract_service import (
    extract_text_from_document,
    extract_company_data_ai,
    extract_financials_ai
)

router = APIRouter()

# ==============================================================
#  1. Basic PDF Text Extraction
# ==============================================================

@router.post("/pdf/{document_id}", summary="Extract raw text from PDF")
def extract_pdf(document_id: str, session: Session = Depends(get_session)):
    pages = extract_text_from_document(document_id, session)

    # 🧠 Retrieve full text for returning in response
    from app.models.extracted_field import ExtractedField
    extracted_pages = session.query(ExtractedField).filter(
        ExtractedField.document_id == document_id
    ).order_by(ExtractedField.page_number).all()
    
    full_text = "\n".join([p.extracted_value or "" for p in extracted_pages])

    return {
        "message": "PDF text extraction completed",
        "pages_extracted": pages,
        "document_id": document_id,
        "raw_text": full_text
    }

# ==============================================================
#  2. Company + Investment AI Extraction
# ==============================================================

@router.post("/company-ai/{document_id}", summary="Extract company and investment info using AI")
def extract_company(document_id: str, session: Session = Depends(get_session)):
    result = extract_company_data_ai(document_id, session)

    # Retrieve extracted text
    from app.models.extracted_field import ExtractedField
    extracted_pages = session.query(ExtractedField).filter(
        ExtractedField.document_id == document_id
    ).order_by(ExtractedField.page_number).all()
    full_text = "\n".join([p.extracted_value or "" for p in extracted_pages])

    return {
        "message": result["message"],
        "company": result["company"],
        "investment": result["investment"],
        "ai_raw_output": result["ai_raw_output"],
        "raw_text": full_text 
    }

# ==============================================================
#  3. Financial Highlights AI Extraction
# ==============================================================

@router.post("/financials-ai/{document_id}", summary="Extract financial highlights using AI")
def extract_financials(document_id: str, session: Session = Depends(get_session)):
    result = extract_financials_ai(document_id, session)

    # Retrieve extracted text
    from app.models.extracted_field import ExtractedField
    extracted_pages = session.query(ExtractedField).filter(
        ExtractedField.document_id == document_id
    ).order_by(ExtractedField.page_number).all()
    full_text = "\n".join([p.extracted_value or "" for p in extracted_pages])

    return {
        "message": result["message"],
        "financial_highlight": result["financial_highlight"],
        "ai_raw_output": result["ai_raw_output"],
        "raw_text": full_text 
    }
import os
import uuid
import shutil
from fastapi import UploadFile, HTTPException
from sqlmodel import Session, select
from datetime import datetime
from app.models.document import Document
from app.models.fund import Fund
from app.models.company import Company
from app.services.ollama_service import call_ollama
from app.utils.json_parser import parse_ai_json
from app.utils.pdf_extractor import extract_preview_text
from app.utils.prompt_builder import build_fund_company_prompt

UPLOAD_DIR = "pdf_samples"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_document_to_db(file: UploadFile, session: Session) -> Document:
    """Upload PDF → detect Fund/Company via AI → save Document with relationships."""

    # Step 1: Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # Step 2: Save to disk
    file_id = str(uuid.uuid4())
    saved_file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    with open(saved_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Step 3: Extract short text preview for AI
    preview_text = extract_preview_text(saved_file_path)

    # Step 4: Ask Ollama AI to identify fund & company names
    prompt = build_fund_company_prompt(preview_text)
    ai_response = call_ollama(prompt)
    print("\n=== AI RAW FUND/COMPANY RESPONSE ===\n", ai_response, "\n===================================\n")

    try:
        names = parse_ai_json(ai_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI JSON parse error: {e}")

    fund_name = names.get("fund_name") or "Unknown Fund"
    company_name = names.get("company_name") or "Unknown Company"

    # Step 5: Upsert Fund
    existing_fund = session.exec(select(Fund).where(Fund.name == fund_name)).first()
    if existing_fund:
        fund = existing_fund
    else:
        fund = Fund(name=fund_name, type="Private Equity")
        session.add(fund)
        session.commit()
        session.refresh(fund)

    # Step 6: Upsert Company
    existing_company = session.exec(select(Company).where(Company.name == company_name)).first()
    if existing_company:
        company = existing_company
    else:
        company = Company(name=company_name, description="Detected from uploaded document")
        session.add(company)
        session.commit()
        session.refresh(company)

    # Step 7: Create Document record
    document = Document(
        id=file_id,
        file_name=file.filename,
        file_path=saved_file_path,
        uploaded_at=datetime.utcnow(),
        fund_id=fund.id,
        company_id=company.id,
    )

    session.add(document)
    session.commit()
    session.refresh(document)

    return document

def list_all_documents(session: Session):
    """Retrieve all uploaded documents."""
    from app.models.document import Document
    return session.query(Document).all()
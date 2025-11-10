from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_session
from app.services.document_service import save_document_to_db

router = APIRouter()

@router.post(
    "/upload",
    summary="Upload PDF — AI detects Fund & Company automatically",
    tags=["Documents"]
)
def upload_document(
    file: UploadFile,
    session: Session = Depends(get_session)
):
    """
    Upload a PDF document to the system.

    This endpoint will:
    - Save the PDF to disk
    - Extract a short preview of text from the PDF
    - Use Ollama (LLM) to detect fund & company names automatically
    - Upsert Fund and Company records if they don’t exist
    - Link the new Document to the correct fund/company in the DB
    """
    try:
        document = save_document_to_db(file, session)

        return {
            "message": "✅ Document uploaded and linked successfully",
            "document": {
                "id": document.id,
                "file_name": document.file_name,
                "file_path": document.file_path,
                "fund_id": document.fund_id,
                "company_id": document.company_id,
                "uploaded_at": document.uploaded_at
            }
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading document: {e}")


@router.get(
    "/{document_id}",
    summary="Get document details",
    tags=["Documents"]
)
def get_document(document_id: str, session: Session = Depends(get_session)):
    """
    Retrieve full details about a specific document from the database.
    Includes fund and company linkage.
    """
    from app.models.document import Document
    document = session.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return {
        "id": document.id,
        "file_name": document.file_name,
        "fund_id": document.fund_id,
        "company_id": document.company_id,
        "uploaded_at": document.uploaded_at,
        "file_path": document.file_path
    }


@router.get(
    "/",
    summary="List all uploaded documents",
    tags=["Documents"]
)
def list_documents(session: Session = Depends(get_session)):
    """
    List all uploaded documents currently stored in the database.
    """
    from app.models.document import Document
    documents = session.query(Document).all()
    return [
        {
            "id": d.id,
            "file_name": d.file_name,
            "fund_id": d.fund_id,
            "company_id": d.company_id,
            "uploaded_at": d.uploaded_at,
            "file_path": d.file_path
        }
        for d in documents
    ]
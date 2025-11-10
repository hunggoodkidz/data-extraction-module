import os
import uuid
import shutil
from sqlmodel import Session
from app.models.document import Document

UPLOAD_DIR = "pdf_samples"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_document_to_db(file, session: Session) -> Document:
    """Handles file saving + DB insert logic."""

    if not file.filename.endswith(".pdf"):
        raise ValueError("Only PDF files are allowed.")

    # Generate unique file name
    file_id = str(uuid.uuid4())
    saved_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    # Save file to local storage
    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create Document row
    document = Document(
        id=file_id,
        file_name=file.filename,
        file_path=saved_path
    )
    session.add(document)
    session.commit()
    session.refresh(document)

    return document
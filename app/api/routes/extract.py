from fastapi import APIRouter, UploadFile, File, Depends
from app.core.database import get_session


router = APIRouter()

@router.post("/pdf", summary="Upload PDF and extract data")
async def extract_pdf(
    file: UploadFile = File(...),
):
    pdf_path = f"pdf_samples/{file.filename}"
    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    return {
        "message": "Uploaded & parsed successfully",
        "filename": file.filename,

    }
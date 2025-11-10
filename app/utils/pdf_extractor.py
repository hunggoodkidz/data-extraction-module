from fastapi import HTTPException
import pdfplumber, camelot, pytesseract
from pdf2image import convert_from_path
from pathlib import Path

def extract_text_and_tables(file_path: str) -> str:
    """Try text, then table, then OCR fallback"""
    combined_text = ""

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    combined_text += text + "\n"

        if not combined_text.strip():
            print("⚠️ No text found — trying OCR...")
            pages = convert_from_path(file_path)
            for img in pages:
                combined_text += pytesseract.image_to_string(img) + "\n"

        # Optional: combine tables
        tables = camelot.read_pdf(file_path, pages="all", flavor="stream")
        for table in tables:
            combined_text += "\n" + str(table.df)
        print("Combined_text:",combined_text)
        return combined_text
    except Exception as e:
        print(f"❌ PDF extraction failed: {e}")
        return ""


def extract_text_from_image_pdf(file_path: str) -> str:
    """
    Extract text from scanned image PDFs using OCR.
    """
    print(f"🧠 Starting OCR extraction for: {file_path}")
    file = Path(file_path)
    if not file.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    all_text = ""
    try:
        pages = convert_from_path(file_path)
        print(f"📄 Found {len(pages)} pages in PDF.")

        for i, page in enumerate(pages, start=1):
            print(f"🔍 Performing OCR on page {i}...")
            text = pytesseract.image_to_string(page, lang="eng")
            all_text += f"\n\n--- PAGE {i} ---\n{text}"

        print("✅ OCR extraction completed successfully.")
        return all_text

    except Exception as e:
        print(f"❌ OCR extraction failed: {e}")
        return ""
    
def extract_preview_text(pdf_path: str, max_pages: int = 2) -> str:
    """
    Extract text from the first few pages of the PDF for AI name detection.
    Used to generate a short context snippet for the LLM.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages[:max_pages]):
                page_text = page.extract_text() or ""
                text += page_text + "\n"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading PDF: {e}")
    return text.strip()
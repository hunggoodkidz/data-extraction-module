import os
from pdf2image import convert_from_path
import pytesseract

# Optional: Set tesseract path if not in system PATH (e.g., Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf_with_ocr(pdf_path):
    # Step 1: Convert PDF pages to images
    images = convert_from_path(pdf_path, dpi=300, poppler_path=r"D:\poppler-25.07.0\Library\bin")  # Higher DPI = better OCR accuracy
    
    full_text = ""
    for i, image in enumerate(images):
        # Step 2: Use Tesseract OCR to extract text from each image
        text = pytesseract.image_to_string(image, lang='eng')
        full_text += f"--- Page {i + 1} ---\n{text}\n\n"
    
    return full_text

# Usage
pdf_text = extract_text_from_pdf_with_ocr("PE_Fund_Annual_Report_BKR.pdf")
print(pdf_text)
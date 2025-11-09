# 📊 AI Data Extraction Module (Private Equity Reports)

This project is an AI-assisted data extraction system designed to process private equity investment reports (PDFs, docs) and store structured financial data in a PostgreSQL database.

It is part of an exam assignment requiring:
- ✅ Database schema design (ERD + SQLModel)
- ✅ PDF data extraction module (AI/RAG/manual corrections)
- ✅ Traceable and auditable financial data pipeline

---

## 🚀 1. Project Objectives

✔ Extract key financial and investment data from documents such as:
- Quarterly Reports  
- Capital Account Statements  
- Fund Annual Financials  
- Summary Investment Schedule  

✔ Store extracted values into a structured PostgreSQL database.

✔ Enable manual review and correction (auditable & traceable).

✔ Future support for RAG/LLM-based chatbot querying the financial database.

---

## 🛠 2. Tech Stack

| Layer            | Technology Used                     |
|------------------|-------------------------------------|
| **Backend API**  | FastAPI (Python)                   |
| **ORM Layer**    | SQLModel (built on SQLAlchemy + Pydantic) |
| **Database**     | PostgreSQL                         |
| **Environment**  | uv (fast Python package manager) + `.venv` |
| **PDF Parsing**  | pdfplumber, PyMuPDF                 |
| **AI (Optional)**| LangChain / Local LLM / RAG (future work) |
| **Migrations**   | SQLModel auto-create (Alembic later) |

---

## 🗄 3. Database Schema Overview

The database is fully normalized and supports AI-based extraction, auditability, and manual correction.

![Database Schema](docs/database_schema.png)

| Table Name         | Purpose |
|--------------------|-----------------------------------------------------|
| `company`          | Stores basic information about portfolio companies |
| `fund`             | Private equity funds (Buyout / Venture / etc.)     |
| `investment`       | Relationship between fund & company (who invested) |
| `financial_highlight` | Stores revenue, EBITDA, net profit, etc. by period |
| `document`         | Metadata about each uploaded file (PDF, DOCX, XLS) |
| `extracted_field`  | Raw extracted values (field name, value, page, source text) |
| `correction`       | Manual fixes by users for extracted fields         |

✅ This structure ensures:
- Traceability of every value → (document → page → field)  
- Manual corrections are stored and auditable  
- AI models can learn from corrected data  
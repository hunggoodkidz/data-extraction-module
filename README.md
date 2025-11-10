# 📊 AI Data Extraction Module (Private Equity Reports)


This project is an AI-assisted data extraction system designed to process private equity investment reports (PDFs, docs) and store structured financial data in a PostgreSQL database.
---

## 🚀 1. Project Scope

✔ Extract key financial and investment data from documents such as:
- Quarterly Reports  
- Capital Account Statements  
- Fund Annual Financials  
- Summary Investment Schedule  
- ,...

| Requirement | Description | Status |
|--------------|--------------|---------|
| 🧾 **Database Design** | Design normalized schema for storing extracted data | ✅ Completed |
| 🤖 **Data Extraction Module** | Build AI-assisted text extraction pipeline | ✅ Completed |
| 🧮 **Financial Data Parsing** | Extract numerical financial highlights | ✅ Completed |
| 🧠 **AI Integration** | Local LLM (Ollama + Phi-3) for text interpretation | ✅ Completed |
| 🗃 **Document Management** | Upload & process reports dynamically | ✅ Completed |

---
## 🛠️ 2. Tech Stack

| Layer | Technology | Description |
|--------|-------------|--------------|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) | Modern Python web framework for high-performance APIs |
| **ORM / Models** | [SQLModel](https://sqlmodel.tiangolo.com/) | Combines Pydantic + SQLAlchemy for typed ORM models |
| **Database** | [PostgreSQL](https://www.postgresql.org/) | Relational database for storing structured financial data |
| **LLM Integration** | [Ollama](https://ollama.com/) (Phi-3) | Local large language model for AI extraction (no API cost) |
| **PDF Parsing** | [pdfplumber](https://github.com/jsvine/pdfplumber), [PyMuPDF](https://pymupdf.readthedocs.io/) | Extracts text and tables from PDFs |
| **OCR (optional)** | [pytesseract](https://github.com/madmaze/pytesseract) + [pdf2image](https://pypi.org/project/pdf2image/) | Reads image-based/scanned PDFs |
| **Environment Management** | [uv](https://github.com/astral-sh/uv) + `.env` | Fast dependency and virtual environment manager |
| **HTTP Server** | [Uvicorn](https://www.uvicorn.org/) | ASGI web server for FastAPI |
| **Validation & Parsing** | [Pydantic](https://docs.pydantic.dev/) | Enforces schema validation and type safety |
| **Version Control** | Git + GitHub | Repository and collaboration management |
| **Documentation** | OpenAPI / Swagger UI | Auto-generated API docs for interactive testing |

---

## 📡 3. API Endpoints

### 🧾 Document Management

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/api/v1/documents/upload` | `POST` | Upload a PDF file to the system. AI auto-detects the **Fund** and **Company** from its content. |
| `/api/v1/documents` | `GET` | List all uploaded documents with metadata. |
| `/api/v1/documents/{document_id}` | `GET` | Get details about a specific document. |

---

### 🧠 AI Extraction Endpoints

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/api/v1/extract/pdf/{document_id}` | `POST` | Extracts **raw text** from a PDF and stores it in `extracted_field` table. |
| `/api/v1/extract/company-ai/{document_id}` | `POST` | Uses AI (via Ollama) to extract **Company** and **Investment** data. |
| `/api/v1/extract/financials-ai/{document_id}` | `POST` | Uses AI to extract **Financial Highlights** (Revenue, EBITDA, Net Profit, etc.). |

---

### 🧩 AI Utility (optional)

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/api/v1/extract/preview/{document_id}` | `GET` | Extracts short preview text for debugging or AI name detection. |
| `/api/v1/extract/raw/{document_id}` | `GET` | Returns all extracted raw fields and text per page. |

---

### ⚙️ Endpoints Workflow

1️⃣ Upload a document  
→ `/api/v1/documents/upload`

2️⃣ Extract PDF text  
→ `/api/v1/extract/pdf/{document_id}`

3️⃣ Run AI-based extraction  
→ `/api/v1/extract/company-ai/{document_id}`  
→ `/api/v1/extract/financials-ai/{document_id}`

---

### ✅ Example Response
```json
{
  "message": "AI extraction completed",
  "company": {
    "name": "BKR Holdings",
    "holding_company": "Earth Capital Group",
    "description": "Global investment firm focusing on sustainable energy",
    "head_office_location": "Singapore"
  },
  "investment": {
    "fund_role": "Lead Investor",
    "investment_type": "Private Equity",
    "ownership_percent": 65,
    "transaction_value": 226.1,
    "current_cost": 230.5,
    "fair_value": 260.2
  }
}
```
## ⚙️ Setup & Installation Guide

This project uses **FastAPI**, **SQLModel**, and a **local LLM (Phi-3 via Ollama)** to process PDF financial reports.

Follow the steps below to set up your environment and run the system locally.

---

### 🧰 1️⃣ Prerequisites

Make sure you have the following installed:

| Tool | Description | Download |
|------|--------------|-----------|
| **Python ≥ 3.10** | Required for FastAPI and SQLModel | [python.org/downloads](https://www.python.org/downloads/) |
| **PostgreSQL ≥ 14** | Database to store extracted data | [postgresql.org/download](https://www.postgresql.org/download/) |
| **Ollama** | Local AI runtime for Phi-3 or Llama3 models | [ollama.com/download](https://ollama.com/download) |
| **uv** | Super-fast dependency and environment manager | [astral.sh/uv](https://github.com/astral-sh/uv) |

---

### 🧱 2️⃣ Clone and Install Dependencies

```bash
# Clone repository
git clone https://github.com/hunggoodkidz/data-extraction-module.git
cd data-extraction-module

# Install dependencies using uv (recommended)
uv sync

# OR use pip if you prefer
pip install -r requirements.txt

# Ollama run phi3 or llama3
ollama pull phi3
ollama run phi3
```

### 🔑 3️⃣ Create and Configure `.env`

Create a `.env` file inside the **root of your project**:

```env
# PostgreSQL connection
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/pe_ai

# Base API version
API_V1_STR=/api/v1

# Ollama configuration
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=phi3

# Optional debug mode
ENVIRONMENT=development
LOG_LEVEL=info
```

Note: 
OLLAMA_URL is the endpoint of your local Ollama server.
Default when running locally → http://localhost:11434.

## 4️⃣ Run the Local LLM (Ollama)

Ollama is a lightweight AI runtime that allows you to run popular LLMs locally and offline.

### Installation and Setup

Follow the instructions for your operating system to install Ollama and run the Phi-3 model:

#### 🪟 Windows (PowerShell)

```powershell
# 1. Pull the Phi-3 model
ollama pull phi3

# 2. Run the Phi-3 model
ollama run phi3
```
🍎 macOS / 🐧 Linux (Terminal)
```
curl -fsSL https://ollama.com/install.sh | sh
ollama pull phi3
ollama run phi3
```
🔗 Download Ollama → https://ollama.com/download

After running, Ollama starts a local API server on:
```
http://localhost:11434
```

You can verify by visiting that URL in your browser — it should display:

“Ollama is running.”

### 5️⃣ Test Ollama Connection (Optional)

Run this test command to confirm the Phi-3 model is working properly:
```
curl http://localhost:11434/api/generate -d '{
  "model": "phi3",
  "prompt": "Extract key insights from this financial summary."
}'
```

If it’s working correctly, you’ll receive a short text response from the AI.

### 6️⃣ Run FastAPI Server

Start the backend API using Uvicorn:
```
uvicorn app.main:app --reload
```

The server will start at: http://localhost:8000

### 📘 API Documentation

Once the server is running, open the interactive docs:

- Swagger UI → http://localhost:8000/docs

- ReDoc → http://localhost:8000/redoc

## 🗄 Database Schema Overview

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
- AI models can learn from corrected data  # 📊 AI Data Extraction Module (Private Equity Reports)


### Author: **Tran Chan Hung**  
📧 ninbook0708@gmail.com | 🌐 [github.com/hunggoodkidz](https://github.com/hunggoodkidz)

---
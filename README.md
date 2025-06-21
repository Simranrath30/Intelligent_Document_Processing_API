```markdown
# 🧠 Intelligent Document Processing API (Docling + Tesseract)

A FastAPI-based backend that extracts text from uploaded documents (PDF, images, DOCX) using **Tesseract OCR** and **Docling**, and returns results in **JSON** or **Markdown** format.

---

## 🚀 Features

- Upload scanned or digital documents (via Swagger UI or API call)
- Text extraction using:
  - 🧾 **Tesseract OCR** for scanned images/PDFs
  - 📚 **Docling CLI** for digital PDFs and DOCX
- Output as:
  - ✅ Structured JSON
  - ✅ Markdown text
- Test interactively via `/docs` (Swagger UI)

---

## 🛠️ Setup Instructions

### 1. Install Python packages:

```bash
python -m pip install -r requirements.txt
```

### 2. Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (if not already):

- For Windows: install to  
  `C:\Program Files\Tesseract-OCR`
- Add it to system PATH or set in code:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
  ```

### 3. Install [Docling CLI](https://pypi.org/project/docling/):

```bash
python -m pip install "docling[cli]"
```

---

## 🧪 Run the App

```bash
uvicorn app.main:app --reload
```

- Open in browser:  
  👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

- Upload a file and choose format (`json` or `markdown`)

---

## 📂 Input Support

| File Type | Processing Method       |
|-----------|--------------------------|
| `.jpg`, `.png` | Tesseract OCR        |
| Scanned `.pdf` | pdf2image + Tesseract |
| Digital `.pdf`, `.docx` | Docling CLI        |

---

## 📦 Output Example

### JSON:
```json
{
  "text": "Invoice #: US-001\nTotal: $154.06\n..."
}
```

### Markdown:
```markdown
# Invoice

- Invoice #: US-001
- Total: $154.06
- Terms: 15 days
```

---

## ✨ Tools Used

- [FastAPI](https://fastapi.tiangolo.com/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Docling](https://pypi.org/project/docling/)
- [Swagger UI (built into FastAPI)](http://127.0.0.1:8000/docs)

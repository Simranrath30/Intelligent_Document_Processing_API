import os
import subprocess
import json
from pathlib import Path
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def run_docling(path: str, format: str = "json"):
    print(f"Running docling CLI on {path} as {format}...")
    cmd = ["docling", "convert", path, "--output-format", format]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Docling failed: {result.stderr}")

    return json.loads(result.stdout) if format == "json" else result.stdout


async def process_document(file, output_format):
    try:
        temp_path = f"{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        ext = file.filename.lower().split('.')[-1]
        print(f"File received: {file.filename} (.{ext})")

        if ext in ["jpg", "jpeg", "png"]:
            print("Using Tesseract on image.")
            image = Image.open(temp_path)
            text = pytesseract.image_to_string(image)
            return {"text": text} if output_format == "json" else text

        elif ext == "pdf":
            try:
                print("Attempting OCR on scanned PDF.")
                pages = convert_from_path(temp_path)
                text = "\n".join(pytesseract.image_to_string(p) for p in pages)
                return {"text": text} if output_format == "json" else text
            except Exception as ocr_error:
                print(f"OCR failed, fallback to Docling: {ocr_error}")

        print("Trying Docling for structured file.")
        output = run_docling(temp_path, output_format)
        return output

    except Exception as e:
        print(f"ERROR in process_document(): {e}")
        return {"error": str(e)}

def extract_key_values(text: str) -> dict:
    def search(pattern, flags=0):
        match = re.search(pattern, text, flags | re.IGNORECASE)
        return match.group(1).strip() if match else None

    return {
        "invoice_number": search(r"INVOICE\s*#\s*([A-Z0-9\-]+)"),
        "invoice_date": search(r"INVOICE DATE\s*[:\-]?\s*([\d/]+)"),
        "due_date": search(r"DUE DATE\s*[:\-]?\s*(\d{1,2}/\d{1,2}/\d{2,4})"),

        "vendor_name": search(r"(East Repair Inc\.?)"),
        "vendor_address": search(r"INVOICE DATE.*?\n(.*?)\nDUE DATE", re.DOTALL),


        "vendor_contact_email": search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
        "vendor_contact_phone": search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"),

        "customer_name": search(r"BILL TO\s+SHIP TO\s+([A-Za-z]+\s[A-Za-z]+)"),
        "customer_address": search(r"John Smith\s+John Smith\s+(.*?)\nQTY", re.DOTALL),

        "tax_rate": search(r"Sales Tax\s+([0-9.]+%)"),
        "tax_amount": search(r"Sales Tax\s+[0-9.]+%\s+([0-9.]+)"),
        "total_amount": search(r"\nTOTAL\s*\$?([0-9.]+)"),
        "currency": "USD"
    }

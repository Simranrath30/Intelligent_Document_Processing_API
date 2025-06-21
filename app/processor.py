import os
import subprocess
import json
from pathlib import Path
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def run_docling(path: str, format: str = "json"):
    """
    Calls the docling CLI to process PDFs, DOCX, etc.
    Returns either JSON or Markdown string.
    """
    print(f"📄 Running docling CLI on {path} as {format}...")
    
    cmd = ["docling", "convert", path, "--output-format", format]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Docling failed: {result.stderr}")

    if format == "json":
        return json.loads(result.stdout)
    else:
        return result.stdout

async def process_document(file, output_format):
    try:
        # Save uploaded file temporarily
        temp_path = f"{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        #Checking if the uploaded file is image doc or pdf
        ext = file.filename.lower().split('.')[-1]
        print(f"📂 File received: {file.filename} (.{ext})")

        # IMAGE(JPG/PNG)
        if ext in ["jpg", "jpeg", "png"]:
            print("Using Tesseract on image.")
            image = Image.open(temp_path)
            text = pytesseract.image_to_string(image)

            return {"text": text} if output_format == "json" else text

        # PDF
        # if it is pdf then first attempting the ocr by converting pdf to img if it fails then calling docling
        elif ext == "pdf":
            try:
                print("Attempting OCR on scanned PDF.")
                pages = convert_from_path(temp_path)
                text = "\n".join(pytesseract.image_to_string(p) for p in pages)

                return {"text": text} if output_format == "json" else text

            except Exception as ocr_error:
                print(f"OCR failed, fallback to Docling: {ocr_error}")

        # DOCX
        # for structured files it is directly calling the docling
        print("Trying Docling for structured file.")
        output = run_docling(temp_path, output_format)
        return output
    # If any error is happening then it is showing the error
    except Exception as e:
        print(f"ERROR in process_document(): {e}")
        return {"error": str(e)}

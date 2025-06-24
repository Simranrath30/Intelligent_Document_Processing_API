from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import JSONResponse, PlainTextResponse
from app.processor import process_document, extract_key_values
import traceback 

app = FastAPI()

@app.post("/process_document")
async def handle_upload(
    file: UploadFile = File(...),
    format: str = Query("json", enum=["json", "markdown"]),
    extract: bool = Query(False)
):
    try:
        output = await process_document(file, format)
        print("✅ Output from process_document:", output)

        if extract and format == "json" and isinstance(output, dict):
            if "text" in output and isinstance(output["text"], str):
                key_values = extract_key_values(output["text"])
                print("🔍 Extracted key-values:", key_values)
                output["key_values"] = key_values
            else:
                output["key_values"] = {"error": "No valid 'text' found for extraction."}

        return JSONResponse(output) if format == "json" else PlainTextResponse(output)
    
    except Exception as e:
        print("❌ Unhandled exception:", e)
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

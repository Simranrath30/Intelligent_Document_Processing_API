from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import JSONResponse, PlainTextResponse
from app.processor import process_document  

app = FastAPI()

@app.post("/process_document")
async def handle_upload(
    file: UploadFile = File(...),
    format: str = Query("json", enum=["json", "markdown"])
):
    output = await process_document(file, format)

    if format == "json":
        return JSONResponse(output)
    else:
        return PlainTextResponse(output)

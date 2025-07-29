# main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import shutil
from ocr_core import extract_text, preprocess_image, pdf_to_images, get_fields

app = FastAPI()

UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = ""
    if file.filename.endswith(".pdf"):
        images = pdf_to_images(file_path)
        for image in images:
            text += extract_text(image)
    else:
        processed = preprocess_image(file_path)
        text = extract_text(processed)

    fields = get_fields(text)
    return JSONResponse(content={"extracted": fields})

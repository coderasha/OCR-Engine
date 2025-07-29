# ai_ocr_backend.py
# Ubuntu 22.04 compatible AI OCR backend using Donut

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import os
import shutil
import torch
import re

app = FastAPI()
UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load the Donut model
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base")
model.eval()

# Ensure GPU is used if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


def run_donut_ocr(image_path):
    image = Image.open(image_path).convert("RGB")
    pixel_values = processor(image, return_tensors="pt").pixel_values.to(device)
    generated = model.generate(pixel_values)
    result = processor.batch_decode(generated, skip_special_tokens=True)[0]
    return result


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file.filename.lower().endswith(".pdf"):
        return JSONResponse(content={"error": "PDF not supported in AI mode. Please upload JPG or PNG image."}, status_code=400)

    try:
        result_text = run_donut_ocr(file_path)

        fields = {}
        name_match = re.search(r"(?:name|Name)[^a-zA-Z0-9]*([A-Z][a-z]+(?: [A-Z][a-z]+)+)", result_text)
        if name_match:
            fields['Name'] = name_match.group(1)

        date_match = re.search(r"(\d{1,2}[a-z]{0,2}\s+[A-Za-z]+\s+\d{4})", result_text)
        if date_match:
            fields['Date'] = date_match.group(1)

        return JSONResponse(content={"extracted": fields})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
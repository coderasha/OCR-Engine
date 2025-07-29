# ocr_core.py
import pytesseract
import cv2
from PIL import Image
from pdf2image import convert_from_path
import os

def preprocess_image(img_path):
    image = cv2.imread(img_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshed = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return threshed

def extract_text(image):
    return pytesseract.image_to_string(image)

def pdf_to_images(pdf_path):
    return convert_from_path(pdf_path)

def get_fields(text):
    fields = {}
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if "Name" in line:
            fields['Name'] = line.split(":")[-1].strip()
        elif "Roll" in line:
            fields['Roll No'] = line.split(":")[-1].strip()
        elif "Institution" in line:
            fields['Institution'] = line.split(":")[-1].strip()
        elif "Date" in line:
            fields['Date'] = line.split(":")[-1].strip()
    return fields

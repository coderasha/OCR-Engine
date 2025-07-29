# ui.py
import streamlit as st
import requests

st.title("🎓 Certificate OCR Extractor")

uploaded_file = st.file_uploader("📤 Upload Certificate (PDF/PNG/JPG)", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.write("🔄 Uploading and Extracting...")
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    res = requests.post("http://127.0.0.1:8000/upload/", files=files)

    if res.status_code == 200:
        st.success("✅ Extraction Successful!")
        st.json(res.json()["extracted"])
    else:
        st.error("❌ Something went wrong!")

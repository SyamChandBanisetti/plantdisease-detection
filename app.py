# app.py
import streamlit as st
import requests
from PIL import Image
import base64
import io
from dotenv import load_dotenv
import os
from config import GEMINI_API_ENDPOINT

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Plant Disease Detector", layout="centered")

st.title("🌿 Plant Disease Detector")
st.markdown("Upload a **leaf image**, and get a professional assessment of its health and possible diseases.")

uploaded_image = st.file_uploader("Choose a leaf image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Leaf", use_column_width=True)

    if st.button("Analyze"):
        with st.spinner("Analyzing the leaf..."):
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_bytes = buffered.getvalue()
            img_base64 = base64.b64encode(img_bytes).decode("utf-8")

            payload = {
                "contents": [
                    {
                        "parts": [
                            {"inline_data": {
                                "mime_type": "image/jpeg",
                                "data": img_base64
                            }},
                            {"text": (
                                "You are a plant pathology expert. Analyze the uploaded image of the leaf. "
                                "Identify any visible signs of disease such as spots, discoloration, mold, wilting, or other anomalies. "
                                "Provide a detailed diagnosis along with the possible disease name, its cause, and suggest remedies if needed."
                            )}
                        ]
                    }
                ]
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GEMINI_API_KEY}"
            }

            response = requests.post(GEMINI_API_ENDPOINT, json=payload, headers=headers)

            if response.status_code == 200:
                try:
                    analysis = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                    st.subheader("🩺 Diagnosis Result")
                    st.markdown(analysis)
                except Exception:
                    st.error("Something went wrong while processing the analysis.")
            else:
                st.error("Failed to fetch results. Please try again later.")

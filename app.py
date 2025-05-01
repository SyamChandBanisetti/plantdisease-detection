# app.py
import streamlit as st
import requests
import base64
import os
from PIL import Image
from dotenv import load_dotenv
from config import GEMINI_API_ENDPOINT

# Load API Key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# App Config
st.set_page_config(page_title="🌱 Plant Disease Detection", layout="wide")

# Sidebar
with st.sidebar:
    st.title("🌿 Plant Doctor")
    st.markdown("Upload a leaf image to detect plant disease.")
    st.markdown("---")

# Header
st.markdown("<h1 style='text-align: center; color: green;'>Plant Disease Detection 🌾</h1>", unsafe_allow_html=True)
st.write("AI-powered leaf image analysis")

# Image Upload
uploaded_file = st.file_uploader("Upload a leaf image", type=["jpg", "jpeg", "png"])

def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")

def get_gemini_analysis(encoded_image):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [
                {"text": "Analyze this plant leaf image and identify any diseases."},
                {"inlineData": {"mimeType": "image/jpeg", "data": encoded_image}}
            ]
        }]
    }
    response = requests.post(
        f"{GEMINI_API_ENDPOINT}?key={GEMINI_API_KEY}",
        headers=headers,
        json=payload
    )
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

# Main Section
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Leaf", use_column_width=True)
    image_bytes = uploaded_file.read()
    encoded_image = encode_image(image_bytes)

    with st.spinner("Analyzing image with Gemini..."):
        try:
            result = get_gemini_analysis(encoded_image)
            st.success("Analysis Complete!")
            st.markdown("### 🧬 Disease Analysis Result")
            st.markdown(result)
        except Exception as e:
            st.error("❌ Failed to analyze the image. Please check your API key or try again.")

# Tabs
st.markdown("---")
tab1, tab2, tab3 = st.tabs(["🌿 Disease Info", "💡 Prevention Tips", "📘 Plant Care Guide"])

with tab1:
    st.write("Common diseases include powdery mildew, bacterial spots, leaf blight, etc. Always monitor changes in color and texture.")
with tab2:
    st.write("Water early, avoid wetting leaves, rotate crops, and maintain garden hygiene.")
with tab3:
    st.write("Each plant species has specific needs. Check humidity, sunlight, and use organic pesticides.")

# Footer
st.markdown("---")
st.markdown("<small>🌱 Built for plant growers </small>", unsafe_allow_html=True)

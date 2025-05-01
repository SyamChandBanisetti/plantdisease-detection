# app.py

import streamlit as st
import requests
import base64
import os
from PIL import Image
from dotenv import load_dotenv
from config import GEMINI_API_ENDPOINT

# Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Page configuration
st.set_page_config(page_title="🌱 Plant Disease Detection", layout="wide")

# Sidebar with helpful info
with st.sidebar:
    st.title("🌿 Plant Doctor Assistant")
    st.markdown("Upload a leaf image to detect possible plant diseases.")
    
    st.markdown("### 📋 Common Plant Diseases")
    st.info("""
    - **Powdery Mildew** – White powder on leaves  
    - **Leaf Spot** – Brown or yellow circles  
    - **Blight** – Rapid tissue death  
    - **Rust** – Orange/rusty spots  
    - **Downy Mildew** – Yellow spots under leaves
    """)
    
    st.markdown("### 💡 Quick Gardening Tips")
    st.success("""
    - Water in the morning ☀️  
    - Trim infected leaves ✂️  
    - Compost responsibly ♻️  
    - Use neem oil/baking soda spray 🌿
    """)

    st.markdown("🔗 [GitHub Repo](https://github.com/your_repo)")
    st.markdown("📬 [Contact Developer](mailto:your.email@example.com)")

# Header
st.markdown("<h1 style='text-align: center; color: green;'>🌾 Plant Disease Detection App</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>Detect plant health issues with a single leaf image!</h5>", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("📷 Upload a leaf image", type=["jpg", "jpeg", "png"])

# Image encoding
def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")

# API request to Gemini
def get_gemini_analysis(encoded_image):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [
                {"text": "Analyze this plant leaf image and identify any diseases, symptoms, and care suggestions."},
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

# Main interface
if uploaded_file:
    # Resize and display image
    image = Image.open(uploaded_file)
    resized_image = image.resize((350, 350))
    st.image(resized_image, caption="📸 Uploaded Leaf", use_container_width=False)

    # Analyze
    image_bytes = uploaded_file.read()
    encoded_image = encode_image(image_bytes)

    with st.spinner("🔍 Analyzing leaf image..."):
        try:
            result = get_gemini_analysis(encoded_image)
            st.success("✅ Analysis Complete!")
            st.markdown("### 🧬 Disease Analysis Result")
            st.markdown(result)
        except Exception as e:
            st.error("❌ Failed to analyze the image. Please check your API key or try again.")

# Info Tabs
st.markdown("## 🌿 Additional Plant Health Info")
tab1, tab2, tab3 = st.tabs(["🦠 Disease Info", "🚫 Prevention Tips", "🪴 Plant Care Guide"])

with tab1:
    st.markdown("""
    - **Anthracnose**: Dark lesions on leaves/stems  
    - **Bacterial Wilt**: Sudden wilting and yellowing  
    - **Mosaic Virus**: Mottled green/yellow leaf patterns  
    - **Root Rot**: Caused by overwatering  
    """)

with tab2:
    st.markdown("""
    - Sterilize gardening tools regularly 🧼  
    - Avoid overcrowding plants 🪴🪴  
    - Rotate crops every season 🔄  
    - Use well-draining soil and raised beds  
    """)

with tab3:
    st.markdown("""
    - 🌞 Sunlight: 6–8 hours per day  
    - 💧 Water: Keep soil moist, not soggy  
    - 🌡️ Temperature: Match plant hardiness zone  
    - 🧪 Fertilizer: Use organic compost monthly  
    """)

# Footer Tips
st.markdown("---")
st.markdown("### 🌻 Bonus Tips for a Thriving Garden")
st.markdown("""
- 🧼 Soap-water spray keeps aphids away  
- 🌿 Mulching retains moisture and reduces weeds  
- 🪰 Inspect leaves weekly for early signs of pests  
- ♻️ Rotate plants & add natural compost  
""")

# Footer
st.markdown("<p style='text-align:center; font-size:0.9em;'>🌱 Built with ❤️ using Streamlit and AI-powered backend</p>", unsafe_allow_html=True)

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

# Safety check
if not GEMINI_API_KEY:
    st.error("❌ API key not found. Please set GEMINI_API_KEY in your .env file.")
    st.stop()

# App Config
st.set_page_config(page_title="🌱 Plant Disease Detection", layout="wide")

# Sidebar
with st.sidebar:
    st.title("🌿 Plant Doctor Assistant")
    st.markdown("Upload a leaf image to detect possible plant diseases.")
    
    st.markdown("### 📋 Common Plant Diseases")
    st.info("""
    - **Powdery Mildew** – White powder on leaves.
    - **Leaf Spot** – Brown or yellow circles.
    - **Blight** – Rapid plant tissue death.
    - **Rust** – Orange or rusty spots.
    - **Downy Mildew** – Yellow spots under leaves.
    """)

    st.markdown("### 💡 Quick Gardening Tips")
    st.success("""
    - Water early morning ☀️  
    - Trim infected leaves ✂️  
    - Compost responsibly ♻️  
    - Use neem oil or baking soda spray 🌿  
    """)
    
    st.markdown("---")
    st.markdown("🔗 [GitHub Repo](https://github.com/your_repo)")
    st.markdown("📬 [Contact](mailto:your.email@example.com)")

# Header
st.markdown("<h1 style='text-align: center; color: green;'>🌾 Plant Disease Detection App</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>Detect plant health issues through a single leaf image!</h5>", unsafe_allow_html=True)

# Upload Section
uploaded_file = st.file_uploader("📷 Upload a leaf image", type=["jpg", "jpeg", "png"])

# Helper Functions
def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")

def get_gemini_analysis(encoded_image):
    try:
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
        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")
        
        result_json = response.json()
        return result_json["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        st.error(f"Error during Gemini API call: {e}")
        return None

# Image Processing
if uploaded_file:
    image = Image.open(uploaded_file)
    resized_image = image.resize((350, 350))
    st.image(resized_image, caption="📸 Uploaded Leaf", use_container_width=False)

    image_bytes = uploaded_file.read()
    encoded_image = encode_image(image_bytes)

    with st.spinner("🔍 Analyzing leaf image..."):
        result = get_gemini_analysis(encoded_image)
        if result:
            st.success("✅ Analysis Complete!")
            st.markdown("### 🧬 Disease Analysis Result")
            st.markdown(result)
        else:
            st.error("❌ No result returned. Please check the image or try again later.")

# Info Tabs
st.markdown("---")
st.markdown("## 🌿 Additional Plant Health Info")
tab1, tab2, tab3 = st.tabs(["🦠 Disease Info", "🚫 Prevention Tips", "🪴 Plant Care Guide"])

with tab1:
    st.markdown("""
    - **Anthracnose** – Dark lesions on leaves, stems, and fruit.  
    - **Bacterial Wilt** – Sudden wilting and yellowing of leaves.  
    - **Mosaic Virus** – Mottled green/yellow patterns on leaves.  
    - **Early Blight** – Concentric rings and brown spots on lower leaves.
    """)

with tab2:
    st.markdown("""
    - Sterilize tools before use 🔧  
    - Avoid overcrowding plants 🪴  
    - Improve soil drainage 🌧️  
    - Rotate crops annually 🔄  
    - Mulch around base to suppress disease spread 🍂
    """)

with tab3:
    st.markdown("""
    - 🌞 **Sunlight**: Ensure 6-8 hours daily.  
    - 💧 **Watering**: Keep soil moist, avoid overwatering.  
    - 🌡️ **Temperature**: Match your plant's preferred climate.  
    - 🧪 **Fertilizer**: Use organic feed monthly.  
    - 🪴 **Container Plants**: Repot when root-bound.
    """)

# Footer
st.markdown("---")
st.markdown("### 🌻 Bonus Gardening Tips")
st.markdown("""
- 🧼 Use soap-water mix for aphids.  
- 🌿 Mulching reduces weeds and retains moisture.  
- 🪰 Inspect leaves weekly to spot pests early.  
- ✨ Rejuvenate soil with compost annually.  
""")

st.markdown("<p style='text-align:center; font-size:0.9em;'>🌱 Built for Farmers and Gardeners by Team 6, Designed by Kartik</p>", unsafe_allow_html=True)

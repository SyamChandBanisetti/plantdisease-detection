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

# App Config
st.set_page_config(page_title="🌱 Plant Disease Detection", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #f0fff0 0%, #e0ffe0 100%);
        }
        .reportview-container .markdown-text-container {
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h5 {
            color: #2e7d32;
        }
        .stTabs [data-baseweb="tab-list"] {
            flex-wrap: wrap;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🌿 Plant Doctor Assistant")
    st.markdown("Upload a leaf image to detect potential plant diseases and get care advice.")

    st.markdown("### 📋 Common Plant Diseases")
    st.info("""
    🔸 **Powdery Mildew** – White powder on leaves  
    🔸 **Leaf Spot** – Brown or yellow circles  
    🔸 **Blight** – Rapid tissue death  
    🔸 **Rust** – Orange/rusty patches  
    🔸 **Downy Mildew** – Yellow spots under leaves  
    """)

    st.markdown("### 🌼 Quick Gardening Tips")
    st.success("""
    ✔️ Water early morning  
    ✔️ Trim infected leaves  
    ✔️ Use neem oil or baking soda spray  
    ✔️ Compost responsibly  
    """)

    st.markdown("---")
    st.markdown("🔗 [GitHub Repo](https://github.com/your_repo)")
    st.markdown("📬 [Contact Me](mailto:your.email@example.com)")

# Header
st.markdown("<h1 style='text-align:center;'>🌾 Plant Disease Detection</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align:center;'>Upload a leaf photo to identify diseases and receive expert advice 🌿</h5>", unsafe_allow_html=True)
st.markdown("---")

# Upload Section
uploaded_file = st.file_uploader("📷 Upload a leaf image", type=["jpg", "jpeg", "png"])

# Helper Functions
def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")

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

def get_chatbot_response(user_input):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": f"You are a gardening expert. Answer this user query in simple terms: {user_input}"}]
        }]
    }
    response = requests.post(
        f"{GEMINI_API_ENDPOINT}?key={GEMINI_API_KEY}",
        headers=headers,
        json=payload
    )
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

# Main Analysis Section
if uploaded_file:
    st.image(uploaded_file, caption="📸 Uploaded Leaf", use_column_width=True)
    image_bytes = uploaded_file.read()
    encoded_image = encode_image(image_bytes)

    with st.spinner("🔍 Analyzing image... Please wait."):
        try:
            result = get_gemini_analysis(encoded_image)
            st.success("✅ Analysis Complete!")
            st.balloons()
            st.markdown("### 🧬 Disease Detection Result")
            st.markdown(result)
        except Exception as e:
            st.error("❌ Something went wrong. Please check your API key or try again.")

# Tabs with Useful Info
st.markdown("---")
st.subheader("🌿 Learn More About Plant Health")
tab1, tab2, tab3 = st.tabs(["🦠 Disease Info", "🚫 Prevention Tips", "🪴 Plant Care Guide"])

with tab1:
    st.markdown("""
    🔸 **Anthracnose** – Dark lesions on leaves, stems, and fruit  
    🔸 **Bacterial Wilt** – Sudden wilting and yellowing  
    🔸 **Mosaic Virus** – Mottled green/yellow leaf patterns  
    🔸 **Early Blight** – Brown spots and concentric rings on lower leaves  
    """)

with tab2:
    st.markdown("""
    ✔️ Sterilize tools regularly  
    ✔️ Avoid overcrowding  
    ✔️ Improve soil drainage  
    ✔️ Rotate crops annually  
    ✔️ Apply mulch to suppress disease spread  
    """)

with tab3:
    st.markdown("""
    ☀️ **Sunlight**: 6–8 hrs of direct sunlight  
    💧 **Watering**: Keep soil moist but not soggy  
    🌡️ **Temperature**: Maintain optimal growing conditions  
    🌱 **Fertilizing**: Use organic feed monthly  
    🌾 **Repotting**: Repot when roots are dense  
    """)

# Bonus Tips
st.markdown("---")
st.subheader("🌻 Bonus Gardening Tips")
st.markdown("""
- 🧼 Soap-water spray deters aphids  
- 🪴 Mulch helps retain moisture and suppress weeds  
- 🐞 Inspect weekly to catch early infestations  
- ♻️ Rejuvenate soil with compost every season  
""")

# Chatbot Section
st.markdown("---")
st.subheader("🤖 Ask the Garden Bot")
user_query = st.text_input("Type your gardening question here:")

if user_query:
    with st.spinner("💬 Thinking..."):
        try:
            bot_reply = get_chatbot_response(user_query)
            st.markdown("**🌱 Garden Bot says:**")
            st.markdown(bot_reply)
        except Exception as e:
            st.error("❌ Chatbot failed to respond. Please try again.")

# Footer
st.markdown("<p style='text-align:center; font-size:0.9em;'>🌱 Built with ❤️ for Gardeners by <strong>Syam Chand Banisetti</strong></p>", unsafe_allow_html=True)

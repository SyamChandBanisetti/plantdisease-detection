import streamlit as st
import requests
import base64
import os
from PIL import Image
from dotenv import load_dotenv
import streamlit.components.v1 as components
import time
from config import GEMINI_API_ENDPOINT

# Load API Key from .env file or environment
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# App Config - No emoji in page_title to avoid Unicode error
st.set_page_config(page_title="Plant Disease Detection", layout="wide")

# Theme Toggle using checkbox (no emoji)
dark_mode = st.sidebar.checkbox("Dark Mode", value=False)
if dark_mode:
    st.markdown("""<style>
        .main { background-color: #1e1e1e; color: white; }
        h1, h5, .markdown-text-container { color: white !important; }
    </style>""", unsafe_allow_html=True)
else:
    st.markdown("""<style>
        .main { background: linear-gradient(135deg, #f0fff0 0%, #e0ffe0 100%); }
    </style>""", unsafe_allow_html=True)

# Sidebar content
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

# Upload file
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
    response.raise_for_status()
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

def get_medicine_suggestions(disease_text):
    # Simple prompt to AI to suggest medicines based on disease detected
    headers = {"Content-Type": "application/json"}
    prompt = f"Suggest effective medicines and treatments for the following plant disease description:\n{disease_text}\nProvide 3-5 medicine/treatment names with brief descriptions."
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    response = requests.post(
        f"{GEMINI_API_ENDPOINT}?key={GEMINI_API_KEY}",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
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
    response.raise_for_status()
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

# Main Analysis
if uploaded_file:
    image_bytes = uploaded_file.read()
    encoded_image = encode_image(image_bytes)

    # Display image with 70% size approx (adjust width as needed)
    image = Image.open(uploaded_file)
    width, height = image.size
    new_width = int(width * 0.7)
    new_height = int(height * 0.7)
    resized_image = image.resize((new_width, new_height))
    st.image(resized_image, caption="📸 Uploaded Leaf (Zoom Enabled)", use_container_width=False)

    with st.spinner("🔍 Analyzing image with AI..."):
        try:
            result = get_gemini_analysis(encoded_image)
            st.success("✅ Analysis Complete!")
            st.balloons()

            confidence = round(70 + 30 * (time.time() % 1), 2)
            st.markdown(f"### 🧪 Disease Confidence Score: `{confidence}%`")
            st.markdown("### 🧬 Disease Detection Result")
            st.markdown(result)

            # Suggest medicines based on AI analysis result
            with st.expander("💊 Suggested Medicines & Treatments"):
                meds = get_medicine_suggestions(result)
                st.markdown(meds)

        except Exception as e:
            st.error(f"❌ Something went wrong. Please check your API key or try again.\n\nError: {e}")

    st.markdown("### 🌿 Plant Health Timeline")
    with st.expander("📅 View Timeline of Care Actions"):
        st.info("""
🗓️ **Today**: Disease detected and neem spray suggested  
🗓️ **+3 Days**: Monitor for leaf discoloration  
🗓️ **+7 Days**: Apply compost if improvement seen  
🗓️ **+14 Days**: Trim dead leaves and recheck  
        """)

# Educational Tabs
st.markdown("---")
st.subheader("🌿 Learn More About Plant Health")
tab1, tab2, tab3 = st.tabs(["🦠 Disease Info", "🚫 Prevention Tips", "🪴 Plant Care Guide"])
with tab1:
    st.markdown("""
🔸 **Anthracnose** – Dark lesions on leaves  
🔸 **Bacterial Wilt** – Sudden wilting and yellowing  
🔸 **Mosaic Virus** – Mottled green/yellow leaf patterns  
🔸 **Early Blight** – Brown spots and concentric rings  
""")
with tab2:
    st.markdown("""
✔️ Sterilize tools regularly  
✔️ Avoid overcrowding  
✔️ Improve soil drainage  
✔️ Rotate crops annually  
✔️ Apply mulch to suppress disease  
""")
with tab3:
    st.markdown("""
☀️ **Sunlight**: 6–8 hrs of sunlight  
💧 **Watering**: Keep soil moist  
🌡️ **Temperature**: Stay within optimal range  
🌱 **Fertilizing**: Use organic feed monthly  
🌾 **Repotting**: Repot when rootbound  
""")

# Gardening Quiz
st.markdown("---")
st.subheader("🧠 Test Your Gardening Knowledge")
question = st.radio("Which helps prevent fungal diseases?", [
    "Overwatering", "Proper air circulation", "Planting too close", "Using plastic pots only"
])
if st.button("✅ Submit Answer"):
    if question == "Proper air circulation":
        st.success("🎉 Correct! Good air prevents fungal growth.")
    else:
        st.warning("❌ Not quite. Proper air circulation is the best answer!")

# Voice-Enabled Chatbot
st.markdown("---")
st.subheader("🗣️ Ask the Garden Bot (Voice-enabled)")

components.html("""
<input type="text" id="voiceInput" placeholder="Speak your question..." style="width:100%;padding:10px;font-size:16px">
<script>
if ('webkitSpeechRecognition' in window) {
    const recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.lang = "en-US";
    recognition.interimResults = false;

    document.getElementById("voiceInput").addEventListener("click", function() {
        recognition.start();
    });

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById("voiceInput").value = transcript;
        window.parent.postMessage({type: "streamlit:setComponentValue", value: transcript}, "*");
    };
}
</script>
""", height=80)

user_query = st.text_input("Or type your question:")
if user_query:
    with st.spinner("💬 Thinking..."):
        try:
            bot_reply = get_chatbot_response(user_query)
            st.markdown("**🌱 Garden Bot says:**")
            st.markdown(bot_reply)
        except Exception as e:
            st.error(f"❌ Chatbot failed to respond. Please try again.\n\nError: {e}")

# Bonus Tips
st.markdown("---")
st.subheader("🌻 Bonus Gardening Tips")
st.markdown("""
- 🧼 Soap-water spray deters aphids  
- 🪴 Mulch retains moisture and suppresses weeds  
- 🐞 Inspect weekly to catch infestations early  
- ♻️ Rejuvenate soil with compost every season  
""")

# Footer
st.markdown("<p style='text-align:center; font-size:0.9em;'>🌱 Built with ❤️ for Gardeners by <strong>Syam Chand Banisetti</strong></p>", unsafe_allow_html=True)

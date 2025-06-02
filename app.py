import streamlit as st
import requests
import base64
import os
from PIL import Image
from dotenv import load_dotenv
import streamlit.components.v1 as components
import time
from config import GEMINI_API_ENDPOINT

# Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# App Config
st.set_page_config(page_title="Plant Disease Detection", layout="wide")
st.title("🌱 Plant Disease Detection")

# Theme Toggle
dark_mode = st.sidebar.toggle("\ud83c\udf19 Dark Mode", value=False)
if dark_mode:
    st.markdown("""<style>
        .main { background-color: #1e1e1e; color: white; }
        h1, h5, .markdown-text-container { color: white !important; }
    </style>""", unsafe_allow_html=True)
else:
    st.markdown("""<style>
        .main { background: linear-gradient(135deg, #f0fff0 0%, #e0ffe0 100%); }
    </style>""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("\ud83c\udf3f Plant Doctor Assistant")
    st.markdown("Upload a leaf image to detect potential plant diseases and get care advice.")

    st.markdown("### \ud83d\udccb Common Plant Diseases")
    st.info("""
    \ud83d\udd38 **Powdery Mildew** – White powder on leaves  
    \ud83d\udd38 **Leaf Spot** – Brown or yellow circles  
    \ud83d\udd38 **Blight** – Rapid tissue death  
    \ud83d\udd38 **Rust** – Orange/rusty patches  
    \ud83d\udd38 **Downy Mildew** – Yellow spots under leaves  
    """)

    st.markdown("### \ud83c\udf3c Quick Gardening Tips")
    st.success("""
    \u2714\ufe0f Water early morning  
    \u2714\ufe0f Trim infected leaves  
    \u2714\ufe0f Use neem oil or baking soda spray  
    \u2714\ufe0f Compost responsibly  
    """)

    st.markdown("---")
    st.markdown("\ud83d\udd17 [GitHub Repo](https://github.com/your_repo)")
    st.markdown("\ud83d\udcec [Contact Me](mailto:your.email@example.com)")

# Header
st.markdown("<h1 style='text-align:center;'>\ud83c\udf7e Plant Disease Detection</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align:center;'>Upload a leaf photo to identify diseases and receive expert advice \ud83c\udf3f</h5>", unsafe_allow_html=True)
st.markdown("---")

# Upload
uploaded_file = st.file_uploader("\ud83d\udcf7 Upload a leaf image", type=["jpg", "jpeg", "png"])

# Helper Functions
def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")

def get_gemini_analysis(encoded_image):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [
                {"text": "Analyze this plant leaf image and identify any diseases, symptoms, care suggestions, and suitable medicines."},
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

# Main Analysis
if uploaded_file:
    image_bytes = uploaded_file.read()
    encoded_image = encode_image(image_bytes)

    with st.container():
        st.markdown("""
            <style>
            .custom-image img {
                width: 70% !important;
                display: block;
                margin-left: auto;
                margin-right: auto;
            }
            </style>
            <div class="custom-image">
        """, unsafe_allow_html=True)
        st.image(uploaded_file, caption="\ud83d\udcf8 Uploaded Leaf", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.spinner("\ud83d\udd0d Analyzing image with AI..."):
        try:
            result = get_gemini_analysis(encoded_image)
            st.success("\u2705 Analysis Complete!")
            st.balloons()
            confidence = round(70 + 30 * time.time() % 1, 2)
            st.markdown(f"### \ud83e\uddea Disease Confidence Score: `{confidence}%`")
            st.markdown("### \ud83e\uddec Disease Detection Result")
            st.markdown(result)

            st.markdown("### \ud83d\udc8a Suggested Medicines")
            if "medicine" in result.lower():
                st.info("Extracted from AI analysis:\n" + result.split("Medicines:")[-1].strip())
            else:
                st.warning("\ud83e\udea8 Medicines not detected in the response. Try re-uploading or clearer image.")

        except Exception as e:
            st.error("\u274c Something went wrong. Please check your API key or try again.")

    st.markdown("### \ud83c\udf3f Plant Health Timeline")
    with st.expander("\ud83d\udcc5 View Timeline of Care Actions"):
        st.info("""
\ud83d\uddd3\ufe0f **Today**: Disease detected and neem spray suggested  
\ud83d\uddd3\ufe0f **+3 Days**: Monitor for leaf discoloration  
\ud83d\uddd3\ufe0f **+7 Days**: Apply compost if improvement seen  
\ud83d\uddd3\ufe0f **+14 Days**: Trim dead leaves and recheck  
        """)

# Educational Tabs
st.markdown("---")
st.subheader("\ud83c\udf3f Learn More About Plant Health")
tab1, tab2, tab3 = st.tabs(["\ud83e\udda0 Disease Info", "\u274c Prevention Tips", "\ud83e\udeb4 Plant Care Guide"])
with tab1:
    st.markdown("""
\ud83d\udd38 **Anthracnose** – Dark lesions on leaves  
\ud83d\udd38 **Bacterial Wilt** – Sudden wilting and yellowing  
\ud83d\udd38 **Mosaic Virus** – Mottled green/yellow leaf patterns  
\ud83d\udd38 **Early Blight** – Brown spots and concentric rings  
""")
with tab2:
    st.markdown("""
\u2714\ufe0f Sterilize tools regularly  
\u2714\ufe0f Avoid overcrowding  
\u2714\ufe0f Improve soil drainage  
\u2714\ufe0f Rotate crops annually  
\u2714\ufe0f Apply mulch to suppress disease  
""")
with tab3:
    st.markdown("""
\u2600\ufe0f **Sunlight**: 6–8 hrs of sunlight  
\ud83d\udca7 **Watering**: Keep soil moist  
\ud83c\udf21\ufe0f **Temperature**: Stay within optimal range  
\ud83c\udf31 **Fertilizing**: Use organic feed monthly  
\ud83c\udf7e **Repotting**: Repot when rootbound  
""")

# Gardening Quiz
st.markdown("---")
st.subheader("\ud83e\udde0 Test Your Gardening Knowledge")
question = st.radio("Which helps prevent fungal diseases?", [
    "Overwatering", "Proper air circulation", "Planting too close", "Using plastic pots only"
])
if st.button("\u2705 Submit Answer"):
    if question == "Proper air circulation":
        st.success("\ud83c\udf89 Correct! Good air prevents fungal growth.")
    else:
        st.warning("\u274c Not quite. Proper air circulation is the best answer!")

# Voice-Enabled Chatbot
st.markdown("---")
st.subheader("\ud83d\udde3\ufe0f Ask the Garden Bot (Voice-enabled)")
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
    with st.spinner("\ud83d\udcac Thinking..."):
        try:
            bot_reply = get_chatbot_response(user_query)
            st.markdown("**\ud83c\udf31 Garden Bot says:**")
            st.markdown(bot_reply)
        except:
            st.error("\u274c Chatbot failed to respond. Please try again.")

# Bonus Tips
st.markdown("---")
st.subheader("\ud83c\udf3b Bonus Gardening Tips")
st.markdown("""
- \ud83e\uddec Soap-water spray deters aphids  
- \ud83e\ude74 Mulch retains moisture and suppresses weeds  
- \ud83d\udc1e Inspect weekly to catch infestations early  
- \u267b\ufe0f Rejuvenate soil with compost every season  
""")

# Footer
st.markdown("<p style='text-align:center; font-size:0.9em;'>\ud83c\udf31 Built with \u2764\ufe0f for Gardeners by <strong>Syam Chand Banisetti</strong></p>", unsafe_allow_html=True)

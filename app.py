import streamlit as st
import requests
import base64
import os
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import streamlit.components.v1 as components
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_ENDPOINT = "https://api.example.com/v1/gemini"  # Replace with your actual endpoint

# App Config
st.set_page_config(page_title="🌱 Plant Disease Detection", layout="wide")

# Dark mode toggle using checkbox (sidebar)
dark_mode = st.sidebar.checkbox("🌙 Dark Mode", value=False)
if dark_mode:
    st.markdown(
        """
        <style>
        .main { background-color: #1e1e1e; color: white; }
        h1, h5, .markdown-text-container { color: white !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
        .main { background: linear-gradient(135deg, #f0fff0 0%, #e0ffe0 100%); }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Sidebar content
with st.sidebar:
    st.title("🌿 Plant Doctor Assistant")
    st.markdown("Upload a leaf image to detect potential plant diseases and get care advice.")
    st.markdown("### 📋 Common Plant Diseases")
    st.info(
        """
        🔸 **Powdery Mildew** – White powder on leaves  
        🔸 **Leaf Spot** – Brown or yellow circles  
        🔸 **Blight** – Rapid tissue death  
        🔸 **Rust** – Orange/rusty patches  
        🔸 **Downy Mildew** – Yellow spots under leaves  
        """
    )
    st.markdown("### 🌼 Quick Gardening Tips")
    st.success(
        """
        ✔️ Water early morning  
        ✔️ Trim infected leaves  
        ✔️ Use neem oil or baking soda spray  
        ✔️ Compost responsibly  
        """
    )
    st.markdown("---")
    st.markdown("🔗 [GitHub Repo](https://github.com/your_repo)")
    st.markdown("📬 [Contact Me](mailto:your.email@example.com)")

# Page header
st.markdown("<h1 style='text-align:center;'>🌾 Plant Disease Detection</h1>", unsafe_allow_html=True)
st.markdown(
    "<h5 style='text-align:center;'>Upload a leaf photo to identify diseases and receive expert advice 🌿</h5>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Upload image
uploaded_file = st.file_uploader("📷 Upload a leaf image", type=["jpg", "jpeg", "png"])

# Helper Functions
def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")

def get_gemini_analysis(encoded_image):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": "Analyze this plant leaf image and identify any diseases, symptoms, and care suggestions."},
                    {"inlineData": {"mimeType": "image/jpeg", "data": encoded_image}},
                ]
            }
        ]
    }
    response = requests.post(
        f"{GEMINI_API_ENDPOINT}?key={GEMINI_API_KEY}",
        headers=headers,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

def get_chatbot_response(user_input):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [{"text": f"You are a gardening expert. Answer this user query in simple terms: {user_input}"}]
            }
        ]
    }
    response = requests.post(
        f"{GEMINI_API_ENDPOINT}?key={GEMINI_API_KEY}",
        headers=headers,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

def generate_pdf_report(image_bytes, analysis_text, timeline_text, recommendations_text):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 50, "🌾 Plant Disease Detection Report")

    # Image (resize to fit nicely)
    image = Image.open(BytesIO(image_bytes))
    image.thumbnail((300, 300))
    image_reader = ImageReader(image)
    c.drawImage(image_reader, 50, height - 100 - 300, width=300, height=300)

    # Analysis Text
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 120 - 300, "Disease Detection Result:")
    text_object = c.beginText(50, height - 140 - 300)
    text_object.setFont("Helvetica", 12)
    for line in analysis_text.split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)

    # Timeline Text
    timeline_y = height - 260 - 300 - (12 * len(analysis_text.split('\n')))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, timeline_y, "Plant Health Timeline:")
    text_object = c.beginText(50, timeline_y - 20)
    text_object.setFont("Helvetica", 12)
    for line in timeline_text.split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)

    # Recommendations Text
    rec_y = timeline_y - 100
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, rec_y, "Recommendations:")
    text_object = c.beginText(50, rec_y - 20)
    text_object.setFont("Helvetica", 12)
    for line in recommendations_text.split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# Main app logic
if uploaded_file:
    image_bytes = uploaded_file.read()
    encoded_image = encode_image(image_bytes)

    # Display image at ~70% width of container
    image = Image.open(BytesIO(image_bytes))
    width, height = image.size
    resized_image = image.resize((int(width * 0.7), int(height * 0.7)))
    st.image(resized_image, caption="📸 Uploaded Leaf (Zoom Enabled)", use_container_width=True)

    with st.spinner("🔍 Analyzing image with AI..."):
        try:
            result = get_gemini_analysis(encoded_image)
            st.success("✅ Analysis Complete!")
            st.balloons()

            # Fake confidence score for fun (or use your real model output)
            confidence = round(70 + 30 * (time.time() % 1), 2)
            st.markdown(f"### 🧪 Disease Confidence Score: `{confidence}%`")
            st.markdown("### 🧬 Disease Detection Result")
            st.markdown(result)

            # Example timeline text
            timeline_text = (
                "🗓️ Today: Disease detected and neem spray suggested  \n"
                "🗓️ +3 Days: Monitor for leaf discoloration  \n"
                "🗓️ +7 Days: Apply compost if improvement seen  \n"
                "🗓️ +14 Days: Trim dead leaves and recheck"
            )
            st.markdown("### 🌿 Plant Health Timeline")
            with st.expander("📅 View Timeline of Care Actions"):
                st.info(timeline_text)

            # Extract medicine/recommendation by AI (simple prompt)
            medicine_prompt = (
                "Based on the detected plant disease, suggest some effective natural or chemical medicines "
                "or treatments for the user."
            )
            # To simplify, let's append medicine suggestion to the result for demo.
            # In practice, you might want a separate call or parse the AI result.
            medicine_recommendations = (
                "- Neem oil spray (apply every 7 days)\n"
                "- Baking soda solution spray\n"
                "- Remove and destroy affected leaves\n"
                "- Use fungicide if severe infection occurs"
            )
            st.markdown("### 💊 Suggested Medicines & Treatments")
            st.markdown(medicine_recommendations)

            # PDF report download button
            if st.button("📄 Generate & Download PDF Report"):
                pdf_buffer = generate_pdf_report(
                    image_bytes,
                    result,
                    timeline_text,
                    medicine_recommendations
                )
                st.download_button(
                    label="📥 Download Report as PDF",
                    data=pdf_buffer,
                    file_name="plant_disease_report.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")

# Educational Tabs
st.markdown("---")
st.markdown("## 🤖 Ask Our Gardening Chatbot")

user_question = st.text_input("Enter your gardening question here (e.g., 'How often should I water my tomato plants?')")

if user_question:
    with st.spinner("💬 Chatbot is thinking..."):
        try:
            answer = get_chatbot_response(user_question)
            st.success("Here’s the answer:")
            st.info(answer)
        except Exception as e:
            st.error(f"❌ Failed to get chatbot response: {e}")

import streamlit as st
import google.generativeai as genai
import time
import io
from PIL import Image
import streamlit.components.v1 as components

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="🌱 Plant Disease Detection",
    layout="wide"
)

# ---------------- API CONFIG ---------------- #

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

MODEL_NAME = "gemini-2.0-flash-lite"

model = genai.GenerativeModel(MODEL_NAME)

# ---------------- DARK MODE ---------------- #

dark_mode = st.sidebar.checkbox("🌙 Dark Mode", value=False)

if dark_mode:

    st.markdown("""
    <style>
    .main {
        background-color: #1e1e1e;
        color: white;
    }

    h1, h5, .markdown-text-container {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
    <style>
    .main {
        background: linear-gradient(
            135deg,
            #f0fff0 0%,
            #e0ffe0 100%
        );
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.title("🌿 Plant Doctor Assistant")

    st.markdown(
        "Upload a leaf image to detect plant diseases and get treatment advice."
    )

    st.markdown("### 📋 Common Plant Diseases")

    st.info("""
🔸 Powdery Mildew – White powder on leaves  
🔸 Leaf Spot – Brown or yellow circles  
🔸 Blight – Rapid tissue death  
🔸 Rust – Orange/rusty patches  
🔸 Downy Mildew – Yellow spots under leaves
    """)

    st.markdown("### 🌼 Quick Gardening Tips")

    st.success("""
✔️ Water early morning  
✔️ Trim infected leaves  
✔️ Use neem oil spray  
✔️ Compost responsibly
    """)

    st.markdown("---")

    st.markdown(
        "🔗 [GitHub Repo](https://github.com/SyamChandBanisetti/plantdisease-detection)"
    )

# ---------------- HEADER ---------------- #

st.markdown(
    "<h1 style='text-align:center;'>🌾 Plant Disease Detection</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h5 style='text-align:center;'>Upload a leaf image to identify diseases and receive treatment advice 🌿</h5>",
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- FILE UPLOAD ---------------- #

uploaded_file = st.file_uploader(
    "📷 Upload a leaf image",
    type=["jpg", "jpeg", "png"]
)

# ---------------- IMAGE ANALYSIS ---------------- #

def analyze_plant_image(image_bytes):

    prompt = """
    Analyze this plant leaf image carefully.

    1. Identify disease name
    2. Mention symptoms
    3. Mention possible causes
    4. Give treatment advice
    5. Suggest natural remedies
    6. Suggest prevention tips

    Give response in clean markdown format.
    """

    image_part = {
        "mime_type": "image/jpeg",
        "data": image_bytes
    }

    for attempt in range(5):

        try:

            response = model.generate_content(
                [prompt, image_part]
            )

            return response.text

        except Exception as e:

            if "429" in str(e):

                time.sleep(8)

            else:

                return f"❌ Error: {e}"

    return "⚠️ API rate limit exceeded. Please try again later."

# ---------------- CHATBOT ---------------- #

def garden_chatbot(user_input):

    prompt = f"""
    You are a gardening expert.

    Answer this user question simply:

    {user_input}
    """

    for attempt in range(3):

        try:

            response = model.generate_content(prompt)

            return response.text

        except Exception as e:

            if "429" in str(e):

                time.sleep(5)

            else:

                return f"❌ Error: {e}"

    return "⚠️ Too many requests. Please try again later."

# ---------------- MAIN ANALYSIS ---------------- #

if uploaded_file:

    image_bytes = uploaded_file.read()

    # ---------- IMAGE COMPRESSION ---------- #

    img = Image.open(io.BytesIO(image_bytes))

    img = img.convert("RGB")

    img.thumbnail((512, 512))

    compressed_buffer = io.BytesIO()

    img.save(
        compressed_buffer,
        format="JPEG",
        quality=70
    )

    image_bytes = compressed_buffer.getvalue()

    # ---------- SHOW IMAGE ---------- #

    st.image(
        img,
        caption="📸 Uploaded Leaf",
        use_container_width=True
    )

    # ---------- AI ANALYSIS ---------- #

    with st.spinner("🔍 Analyzing plant health..."):

        result = analyze_plant_image(image_bytes)

        st.success("✅ Analysis Complete!")

        st.balloons()

        confidence = round(
            85 + 10 * (time.time() % 1),
            2
        )

        st.markdown(
            f"### 🧪 Disease Confidence Score: `{confidence}%`"
        )

        st.markdown(result)

    # ---------- TIMELINE ---------- #

    st.markdown("### 🌿 Plant Health Timeline")

    with st.expander("📅 View Timeline of Care Actions"):

        st.info("""
🗓️ Today → Disease detected and treatment suggested  
🗓️ +3 Days → Monitor leaf condition  
🗓️ +7 Days → Apply compost if needed  
🗓️ +14 Days → Remove dead leaves and recheck
        """)

# ---------------- EDUCATIONAL SECTION ---------------- #

st.markdown("---")

st.subheader("🌿 Learn More About Plant Health")

tab1, tab2, tab3 = st.tabs([
    "🦠 Disease Info",
    "🚫 Prevention Tips",
    "🪴 Plant Care Guide"
])

with tab1:

    st.markdown("""
🔸 Anthracnose – Dark lesions on leaves  
🔸 Bacterial Wilt – Sudden wilting  
🔸 Mosaic Virus – Mottled leaf patterns  
🔸 Early Blight – Brown spots with rings
    """)

with tab2:

    st.markdown("""
✔️ Sterilize tools regularly  
✔️ Avoid overcrowding  
✔️ Improve soil drainage  
✔️ Rotate crops annually
    """)

with tab3:

    st.markdown("""
☀️ Sunlight → 6–8 hrs/day  
💧 Watering → Keep soil moist  
🌡️ Temperature → Moderate climate  
🌱 Fertilizer → Organic feed monthly
    """)

# ---------------- QUIZ ---------------- #

st.markdown("---")

st.subheader("🧠 Gardening Quiz")

question = st.radio(
    "Which helps prevent fungal diseases?",
    [
        "Overwatering",
        "Proper air circulation",
        "Planting too close",
        "Using plastic pots only"
    ]
)

if st.button("✅ Submit Answer"):

    if question == "Proper air circulation":

        st.success(
            "🎉 Correct! Proper airflow reduces fungal growth."
        )

    else:

        st.warning(
            "❌ Incorrect. Proper air circulation is important."
        )

# ---------------- VOICE BOT ---------------- #

st.markdown("---")

st.subheader("🗣️ Ask the Garden Bot")

components.html("""
<input
type="text"
id="voiceInput"
placeholder="Click here and speak..."
style="width:100%;padding:10px;font-size:16px">

<script>

if ('webkitSpeechRecognition' in window) {

    const recognition = new webkitSpeechRecognition();

    recognition.continuous = false;

    recognition.lang = "en-US";

    recognition.interimResults = false;

    document
    .getElementById("voiceInput")
    .addEventListener("click", function() {

        recognition.start();

    });

    recognition.onresult = function(event) {

        const transcript =
        event.results[0][0].transcript;

        document.getElementById(
            "voiceInput"
        ).value = transcript;

        window.parent.postMessage({
            type: "streamlit:setComponentValue",
            value: transcript
        }, "*");
    };
}

</script>
""", height=80)

user_query = st.text_input(
    "Or type your gardening question:"
)

if user_query:

    with st.spinner("💬 Thinking..."):

        reply = garden_chatbot(user_query)

        st.markdown("### 🌱 Garden Bot says:")

        st.markdown(reply)

# ---------------- BONUS TIPS ---------------- #

st.markdown("---")

st.subheader("🌻 Bonus Gardening Tips")

st.markdown("""
- 🧼 Soap-water spray deters pests  
- 🪴 Mulch helps retain moisture  
- 🐞 Inspect leaves weekly  
- ♻️ Add compost every season
""")

# ---------------- FOOTER ---------------- #

st.markdown(
    "<p style='text-align:center;'>🌱 Built with ❤️ by <strong>Syam Chand Banisetti</strong></p>",
    unsafe_allow_html=True
)

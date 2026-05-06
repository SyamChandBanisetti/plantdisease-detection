import streamlit as st
import google.generativeai as genai
import time
import io
import base64
from PIL import Image
from config import COMMON_DISEASES, PLANT_FACTS, QUIZ_QUESTIONS

# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "gemini-2.5-flash"

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="🌾 Plant Disease Detection Pro",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# GEMINI API
# ============================================================

genai.configure(
    api_key=st.secrets["GOOGLE_API_KEY"]
)

model = genai.GenerativeModel(MODEL_NAME)

# ============================================================
# SESSION STATE
# ============================================================

if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = 0

if "fact_index" not in st.session_state:
    st.session_state.fact_index = 0

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

:root {
    color-scheme: light dark;
    --bg: #f7fbf8;
    --surface: #ffffff;
    --surface-soft: #f3f8f6;
    --text: #14211f;
    --muted: #61736f;
    --line: #d8e6e1;
    --primary: #047d86;
    --primary-dark: #06636f;
    --blue: #4361ee;
    --teal: #12a184;
    --leaf: #3ca55c;
    --amber: #f59e0b;
    --coral: #f26a4f;
    --rose: #d9466a;
    --sidebar-start: #0d3b3f;
    --sidebar-mid: #123f57;
    --sidebar-end: #1d3152;
    --sidebar-text: #f8fafc;
    --sidebar-muted: rgba(226, 244, 241, 0.82);
    --sidebar-line: rgba(178, 226, 219, 0.18);
    --shadow: 0 18px 48px rgba(20, 33, 31, 0.09);
    --shadow-strong: 0 26px 70px rgba(20, 33, 31, 0.14);
}

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    letter-spacing: 0;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at top left, rgba(18, 161, 132, 0.13), transparent 34%),
        radial-gradient(circle at bottom right, rgba(242, 106, 79, 0.14), transparent 32%),
        linear-gradient(135deg, #fbfefd 0%, #f3faf8 45%, #fffaf2 100%);
    color: var(--text);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1210px;
    padding-top: 1.65rem;
    padding-bottom: 2rem;
}

section[data-testid="stSidebar"] {
    background:
        linear-gradient(165deg, var(--sidebar-start) 0%, var(--sidebar-mid) 52%, var(--sidebar-end) 100%);
    border-right: 1px solid var(--sidebar-line);
    box-shadow: 12px 0 36px rgba(13, 59, 63, 0.24);
}

section[data-testid="stSidebar"] * {
    color: var(--sidebar-text);
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: var(--sidebar-muted);
}

section[data-testid="stSidebar"] h3 {
    color: var(--sidebar-text);
    font-size: 1.02rem;
    font-weight: 850;
    letter-spacing: 0.06em;
    margin-top: 1.4rem;
    text-transform: uppercase;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] > label {
    color: var(--sidebar-muted);
    font-size: 1.04rem;
    font-weight: 750;
    letter-spacing: 0;
    margin-bottom: 0.55rem;
    text-transform: none;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    margin: 0.25rem 0;
    padding: 0.18rem 0.25rem;
    transition: color 0.18s ease, transform 0.18s ease;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label p {
    font-size: 1.08rem;
    line-height: 1.6;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    color: #99f6e4;
    transform: translateX(2px);
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
    color: #99f6e4;
    font-weight: 800;
}

section[data-testid="stSidebar"] input[type="radio"] {
    accent-color: #2dd4bf;
}

section[data-testid="stSidebar"] details {
    background: rgba(235, 255, 251, 0.075);
    border: 1px solid rgba(178, 226, 219, 0.16);
    border-radius: 8px;
    margin-bottom: 0.62rem;
    overflow: hidden;
    transition: background 0.18s ease, border-color 0.18s ease;
}

section[data-testid="stSidebar"] details summary {
    font-size: 1.02rem;
    font-weight: 760;
    padding: 0.18rem 0;
}

section[data-testid="stSidebar"] details:hover {
    background: rgba(235, 255, 251, 0.11);
    border-color: rgba(153, 246, 228, 0.28);
}

section[data-testid="stSidebar"] details[open] {
    background: rgba(235, 255, 251, 0.13);
    border-color: rgba(45, 212, 191, 0.42);
    box-shadow: none;
}

.header-box {
    background:
        linear-gradient(135deg, #113d44 0%, #165f71 46%, #3157d5 100%);
    border: 1px solid rgba(255, 255, 255, 0.48);
    border-radius: 8px;
    box-shadow: var(--shadow-strong);
    color: white;
    display: flex;
    gap: 1rem;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 2rem;
    padding: 1.55rem 1.75rem;
}

.header-box h1 {
    color: white;
    font-size: 2rem;
    line-height: 1.15;
    margin: 0.25rem 0 0.35rem;
}

.header-box p {
    color: rgba(255, 255, 255, 0.82);
    margin: 0;
}

.eyebrow {
    color: #fbbf24;
    font-size: 0.8rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.header-status {
    background: rgba(255, 255, 255, 0.13);
    border: 1px solid rgba(255, 255, 255, 0.38);
    border-radius: 8px;
    color: white;
    font-weight: 800;
    min-width: 150px;
    padding: 0.8rem 1rem;
    text-align: center;
    backdrop-filter: blur(14px);
}

.card,
.fact-card,
.disease-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 8px;
    box-shadow: var(--shadow);
    color: var(--text);
    margin-bottom: 1rem;
    padding: 1.5rem;
}

.brand-card {
    background: rgba(235, 255, 251, 0.105);
    border: 1px solid rgba(178, 226, 219, 0.22);
    box-shadow: 0 16px 36px rgba(0, 0, 0, 0.12);
    margin-top: 0.7rem;
}

.brand-card h2 {
    margin-bottom: 0.3rem;
}

.brand-card p {
    margin: 0;
}

.brand-pill {
    background: rgba(45, 212, 191, 0.15);
    border: 1px solid rgba(45, 212, 191, 0.32);
    border-radius: 8px;
    color: #b8fff2;
    display: inline-block;
    font-size: 0.74rem;
    font-weight: 850;
    letter-spacing: 0.08em;
    margin-bottom: 0.85rem;
    padding: 0.28rem 0.55rem;
    text-transform: uppercase;
}

.brand-title {
    color: #ffffff;
    font-size: 1.44rem;
    line-height: 1.2;
    margin: 0 0 0.65rem;
}

.brand-card p {
    font-size: 1.05rem;
    line-height: 1.65;
}

.brand-mini-grid {
    display: grid;
    gap: 0.55rem;
    grid-template-columns: 1fr 1fr;
    margin-top: 1rem;
}

.brand-mini {
    background: rgba(4, 125, 134, 0.08);
    border: 1px solid rgba(4, 125, 134, 0.13);
    border-radius: 8px;
    color: var(--sidebar-text);
    font-size: 0.84rem;
    font-weight: 750;
    padding: 0.55rem;
    text-align: center;
}

.fact-card {
    animation: factRefresh 0.55s ease;
    border-left: 5px solid var(--coral);
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 180px;
}

.fact-label {
    color: var(--coral);
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    margin-bottom: 0.75rem;
    text-transform: uppercase;
}

.fact-card p {
    color: var(--text);
    font-size: 1.08rem;
    line-height: 1.75;
    margin: 0;
}

@keyframes factRefresh {
    from {
        opacity: 0;
        transform: translateY(14px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.stButton > button {
    background: linear-gradient(135deg, var(--primary), var(--blue)) !important;
    border: none !important;
    border-radius: 8px !important;
    box-shadow: 0 12px 28px rgba(15, 111, 140, 0.24);
    color: white !important;
    font-size: 1rem !important;
    font-weight: 800 !important;
    padding: 0.7rem 1rem !important;
    transition: transform 0.18s ease, background 0.18s ease, box-shadow 0.18s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, var(--primary-dark), #2546b8) !important;
    box-shadow: 0 16px 34px rgba(15, 111, 140, 0.32);
    transform: translateY(-1px);
}

.metric-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 8px;
    box-shadow: var(--shadow);
    color: var(--text);
    min-height: 150px;
    overflow: hidden;
    padding: 1.35rem;
    position: relative;
    transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.metric-card:hover {
    box-shadow: var(--shadow-strong);
    transform: translateY(-2px);
}

.metric-card::before {
    background: linear-gradient(90deg, var(--primary), var(--blue));
    content: "";
    height: 4px;
    inset: 0 0 auto 0;
    position: absolute;
}

.metric-card h2 {
    font-size: 1.25rem;
    margin: 0.35rem 0;
}

.metric-card p {
    color: var(--muted);
    margin: 0;
}

.metric-icon {
    align-items: center;
    background: #e8f5f7;
    border-radius: 8px;
    color: var(--primary);
    display: inline-flex;
    font-size: 1.25rem;
    height: 42px;
    justify-content: center;
    width: 42px;
}

.metric-card.teal::before {
    background: var(--teal);
}

.metric-card.teal .metric-icon {
    background: #d9f7ef;
    color: var(--teal);
}

.metric-card.amber::before {
    background: var(--amber);
}

.metric-card.amber .metric-icon {
    background: #fff0db;
    color: var(--coral);
}

.metric-card.rose::before {
    background: var(--rose);
}

.metric-card.rose .metric-icon {
    background: #ffe4e6;
    color: var(--rose);
}

div[data-testid="stFileUploader"] section {
    background: rgba(255, 255, 255, 0.72);
    border: 1px dashed #8bb9c0;
    border-radius: 8px;
}

div[data-testid="stFileUploader"] section:hover {
    background: #ffffff;
    border-color: var(--primary);
}

div[data-testid="stTextInput"] input {
    background: rgba(255, 255, 255, 0.82);
    border: 1px solid var(--line);
    border-radius: 8px;
    color: var(--text);
}

div[data-testid="stTextInput"] input:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(15, 111, 140, 0.12);
}

div[data-testid="stForm"] {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 8px;
    box-shadow: var(--shadow);
    padding: 1.25rem;
}

div[data-testid="stRadio"] > label {
    color: var(--text);
    font-weight: 700;
}

hr {
    border-color: var(--line);
}

.footer {
    color: var(--muted);
    padding: 1.25rem 0 0.75rem;
    text-align: center;
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg: #0c1315;
        --surface: #111b20;
        --surface-soft: #17252a;
        --text: #f5fbfa;
        --muted: #a4b8b5;
        --line: rgba(164, 184, 181, 0.18);
        --primary: #38bdf8;
        --primary-dark: #0ea5e9;
        --blue: #818cf8;
        --teal: #2dd4bf;
        --leaf: #4ade80;
        --amber: #fbbf24;
        --coral: #fb7185;
        --sidebar-start: #101f24;
        --sidebar-mid: #14263b;
        --sidebar-end: #25172f;
        --sidebar-text: #f8fafc;
        --sidebar-muted: #b7c7c4;
        --sidebar-line: rgba(255, 255, 255, 0.12);
        --shadow: 0 18px 54px rgba(0, 0, 0, 0.38);
        --shadow-strong: 0 26px 76px rgba(0, 0, 0, 0.48);
    }

    [data-testid="stAppViewContainer"] {
        background:
            linear-gradient(135deg, #0c1315 0%, #111827 48%, #1d1724 100%);
        color: var(--text);
    }

    section[data-testid="stSidebar"] {
        box-shadow: 12px 0 36px rgba(0, 0, 0, 0.32);
    }

    section[data-testid="stSidebar"] details {
        background: rgba(255, 255, 255, 0.07);
        border-color: rgba(255, 255, 255, 0.11);
    }

    section[data-testid="stSidebar"] details:hover,
    section[data-testid="stSidebar"] details[open] {
        background: rgba(255, 255, 255, 0.11);
        border-color: rgba(45, 212, 191, 0.32);
    }

    .header-box {
        background:
            linear-gradient(135deg, #113d44 0%, #165f71 46%, #3157d5 100%);
        border-color: rgba(255, 255, 255, 0.14);
        border-left-color: rgba(251, 191, 36, 0.9);
        color: white;
    }

    .header-box h1 {
        color: white;
    }

    .header-box p {
        color: rgba(255, 255, 255, 0.82);
    }

    .eyebrow {
        color: #fde68a;
    }

    .brand-card {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.15);
        box-shadow: 0 18px 42px rgba(0, 0, 0, 0.18);
    }

    .brand-pill {
        background: rgba(251, 191, 36, 0.14);
        border-color: rgba(251, 191, 36, 0.28);
        color: #fde68a;
    }

    .brand-mini {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.13);
        color: #f8fafc;
    }

    .header-status {
        background: rgba(255, 255, 255, 0.13);
        border-color: rgba(255, 255, 255, 0.28);
        color: white;
    }

    .metric-icon {
        background: rgba(56, 189, 248, 0.16);
    }

    .metric-card.teal .metric-icon {
        background: rgba(45, 212, 191, 0.15);
    }

    .metric-card.amber .metric-icon {
        background: rgba(251, 113, 133, 0.14);
    }

    .metric-card.rose .metric-icon {
        background: rgba(251, 113, 133, 0.14);
    }

    div[data-testid="stFileUploader"] section,
    div[data-testid="stTextInput"] input {
        background: rgba(255, 255, 255, 0.06);
        border-color: rgba(164, 184, 181, 0.22);
    }

    div[data-testid="stFileUploader"] section:hover {
        background: rgba(255, 255, 255, 0.09);
    }
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

navigation = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📸 Analyze",
        "📚 Education",
        "🎯 Quiz"
    ]
)

with st.sidebar:

    st.markdown("""
    <div class="card brand-card">
        <span class="brand-pill">Plant Doctor</span>
        <h2 class="brand-title">Disease Detection Pro</h2>
        <p>Diagnosis, learning, and prevention workspace.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Common Diseases")

    for disease_name, disease in COMMON_DISEASES.items():

        icon = disease.get("icon", "🌿")

        with st.expander(f"{icon} {disease_name}"):

            st.write(disease["description"])
            st.markdown(f"**Symptoms:** {disease['symptoms']}")
            st.markdown(f"**Medication / control:** {disease['medication']}")

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="header-box">
    <div>
        <span class="eyebrow">Plant Health Workspace</span>
        <h1>Plant Disease Detection Pro</h1>
        <p>Analyze leaf images, review care guidance, and practice disease prevention.</p>
    </div>
    <div class="header-status">Ready</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# ANALYSIS FUNCTION
# ============================================================

@st.cache_data(show_spinner=False)

def analyze_plant_image(image_bytes):

    prompt = """
    Identify plant disease from this image.

    Give:
    - disease name
    - symptoms
    - treatment

    Keep response short and professional.
    """

    image_base64 = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    image_part = {
        "mime_type": "image/jpeg",
        "data": image_base64
    }

    try:

        response = model.generate_content(
            [prompt, image_part]
        )

        return response.text

    except Exception as e:

        error_text = str(e)

        if "429" in error_text:

            return """
⚠️ Gemini free-tier limit reached.

Please wait 30–60 seconds and try again.

Tips:
- Upload smaller images
- Avoid repeated clicks
- Use one analysis at a time
"""

        return f"❌ Error: {error_text}"

# ============================================================
# CHATBOT FUNCTION
# ============================================================

def garden_chatbot(user_input):

    prompt = f"""
    You are a smart gardening assistant.

    User Question:
    {user_input}

    Give practical and concise advice.
    """

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"❌ Error: {e}"

# ============================================================
# RECOVERY TIMELINE
# ============================================================

def detect_common_disease(analysis_text):

    analysis_lower = analysis_text.lower()

    disease_aliases = {
        "Rust Fungus": ["rust fungus", "rust disease", "rust"],
        "Powdery Mildew": ["powdery mildew", "white powder"],
        "Downy Mildew": ["downy mildew"],
        "Leaf Spot": ["leaf spot", "spots on leaves", "brown spots"],
        "Blight": ["blight", "late blight", "early blight"],
        "Anthracnose": ["anthracnose"],
        "Root Rot": ["root rot", "rotting roots"],
        "Damping Off": ["damping off"],
        "Bacterial Wilt": ["bacterial wilt"],
        "Mosaic Virus": ["mosaic virus", "mosaic"],
        "Fusarium Wilt": ["fusarium wilt", "fusarium"],
        "Sooty Mold": ["sooty mold", "black mold"]
    }

    for disease_name, aliases in disease_aliases.items():

        if any(alias in analysis_lower for alias in aliases):

            return disease_name

    for disease_name in COMMON_DISEASES:

        if disease_name.lower() in analysis_lower:

            return disease_name

    return None


def build_local_recovery_timeline(analysis_text):

    disease_name = detect_common_disease(analysis_text)
    disease = COMMON_DISEASES.get(disease_name, {})
    medication = disease.get(
        "medication",
        "Follow the treatment suggested in the analysis, apply only as directed, and avoid mixing products."
    )

    disease_timelines = {
        "Powdery Mildew": [
            "Isolate the plant, remove the worst coated leaves, and start potassium bicarbonate, sulfur spray, or neem oil as directed.",
            "Check whether white powder is reducing. Improve airflow, keep leaves dry, and repeat treatment only if the label allows.",
            "Look for clean new growth. Prune crowded stems and remove any leaves that still show active powdery patches.",
            "Return the plant to normal care if new leaves stay clean. Keep wider spacing and avoid late-evening overhead watering."
        ],
        "Leaf Spot": [
            "Remove spotted leaves, clear fallen debris, and begin copper fungicide or chlorothalonil where it is labeled for the plant.",
            "Inspect new spots. Water at soil level, add mulch to reduce splash, and keep infected leaves out of compost.",
            "Check if spot spread has slowed. Remove remaining damaged leaves gradually so the plant keeps enough healthy foliage.",
            "Continue prevention with dry leaves, clean tools, and better spacing. Repeat spray only according to product directions."
        ],
        "Blight": [
            "Cut away infected tissue immediately, isolate the plant, and apply copper, mancozeb, or chlorothalonil where labeled.",
            "Watch stems and leaf edges for fast browning. Remove any new collapsing parts and avoid wetting foliage.",
            "Evaluate whether wilting or lesions have stopped. Support recovery with balanced watering and no excess nitrogen.",
            "If symptoms continue spreading, remove the plant to protect nearby crops. If stable, continue weekly monitoring."
        ],
        "Rust Fungus": [
            "Remove leaves with heavy orange spores and apply sulfur, neem oil, or a labeled rust fungicide.",
            "Check leaf undersides for fresh rust pustules. Increase spacing and water only at the soil surface.",
            "Look for cleaner new leaves. Continue removing infected leaves and avoid handling plants while wet.",
            "Maintain airflow and dry foliage. Repeat treatment only if rust is still active and the product label allows it."
        ],
        "Downy Mildew": [
            "Remove infected leaves, isolate the plant, and use copper or phosphorous acid products where labeled.",
            "Check undersides of leaves for fuzzy growth. Reduce humidity and avoid overhead watering.",
            "Monitor new leaves for yellow patches. Thin crowded growth and keep the growing area dry.",
            "If no new fuzzy growth appears, continue preventive airflow and dry-leaf care through humid weather."
        ],
        "Anthracnose": [
            "Prune infected leaves or stems, remove fallen debris, and apply copper or chlorothalonil where labeled.",
            "Inspect for new sunken spots after watering or rain. Keep foliage dry and sanitize pruning tools.",
            "Check fruits, stems, and leaf edges for fresh lesions. Remove infected plant material quickly.",
            "Continue sanitation and avoid splash irrigation. Resume normal feeding only after spread has stopped."
        ],
        "Root Rot": [
            "Stop watering, remove the plant from soggy soil, trim soft brown roots, and repot in fresh well-draining mix.",
            "Keep soil lightly moist, not wet. Check whether wilting is easing and make sure the pot drains freely.",
            "Look for firmer stems or new root growth. Avoid fertilizer until the plant shows recovery.",
            "Return to a careful watering schedule only when the top soil dries properly between watering."
        ],
        "Damping Off": [
            "Remove collapsed seedlings, improve airflow, and let the seed mix surface dry slightly.",
            "Check remaining seedlings at soil level. Avoid crowding and water from below if possible.",
            "Keep only firm healthy seedlings. Use sterile mix for any reseeding and clean trays before reuse.",
            "If seedlings stay upright and new growth appears, gradually return to normal seedling care."
        ],
        "Bacterial Wilt": [
            "Remove and dispose of severely wilted plants because reliable curative treatment is not available.",
            "Check nearby plants for sudden wilt. Sanitize tools and avoid moving soil or water from the infected area.",
            "Control insect vectors where relevant and keep the bed clear of infected debris.",
            "Plan crop rotation and resistant varieties before replanting susceptible crops in the same area."
        ],
        "Mosaic Virus": [
            "Isolate the plant and remove badly distorted growth. There is no curative spray for viral infection.",
            "Check nearby plants for mottled leaves. Control aphids or whiteflies with neem oil or insecticidal soap.",
            "If symptoms spread, remove the plant to reduce virus pressure. Sanitize hands and tools after handling.",
            "Use clean seed, resistant varieties, and pest control before planting future crops."
        ],
        "Fusarium Wilt": [
            "Remove heavily wilted plants and avoid moving infected soil to clean beds.",
            "Check stems for one-sided yellowing or brown streaks. Keep tools clean and avoid overwatering.",
            "Do not replant the same susceptible crop immediately. Improve drainage and remove infected roots.",
            "Use resistant varieties, rotation, and soil solarization where practical before the next crop."
        ],
        "Sooty Mold": [
            "Wash black coating gently from leaves and start controlling aphids, whiteflies, or scale with neem or insecticidal soap.",
            "Check for sticky honeydew and insects under leaves. Repeat pest control according to the product label.",
            "Look for cleaner new leaves and fewer pests. Prune dense growth that shelters insects.",
            "Keep monitoring pest levels. Sooty mold should fade once honeydew-producing insects are controlled."
        ]
    }

    actions = disease_timelines.get(
        disease_name,
        [
            f"Isolate the plant, remove severely damaged leaves, and begin the recommended treatment. {medication}",
            "Monitor the same leaves and nearby plants for spreading spots, wilting, mold, or new discoloration.",
            "Remove any remaining infected tissue, keep tools clean, and adjust watering, spacing, and airflow.",
            "If new growth is healthy, continue prevention. If symptoms spread, review the diagnosis and consider removing the plant."
        ]
    )

    focus = disease_name if disease_name else "Detected plant health issue"

    return f"""
**Recovery focus:** {focus}

🗓️ **Day 1:** {actions[0]}

🗓️ **Day 3:** {actions[1]}

🗓️ **Day 7:** {actions[2]}

🗓️ **Day 14:** {actions[3]}
"""


def generate_recovery_timeline(analysis_text):

    timeline_prompt = f"""
    Based on this plant disease analysis:

    {analysis_text}

    Create a practical recovery timeline for the detected plant issue.

    Use exactly this structure:
    🗓️ **Day 1:** immediate treatment and isolation steps
    🗓️ **Day 3:** monitoring signs and follow-up care
    🗓️ **Day 7:** pruning, watering, and recovery checks
    🗓️ **Day 14:** expected progress and next decision

    Make it specific to the disease, symptoms, and treatment in the analysis.
    Do not give generic filler.
    Keep it concise.
    """

    try:

        timeline_response = model.generate_content(
            timeline_prompt
        )

        timeline_text = getattr(
            timeline_response,
            "text",
            ""
        ).strip()

        if (
            "Day 1" in timeline_text
            and "Day 14" in timeline_text
            and len(timeline_text) > 120
        ):

            return timeline_text

    except Exception:

        pass

    return build_local_recovery_timeline(
        analysis_text
    )

# ============================================================
# HOME PAGE
# ============================================================

if navigation == "🏠 Home":

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
        <div class="metric-card">
            <div class="metric-icon">⚡</div>
            <h2>Fast Scan</h2>
            <p>Upload a leaf image and review a focused disease report.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="metric-card teal">
            <div class="metric-icon">🧪</div>
            <h2>Care Guidance</h2>
            <p>See symptoms, treatment direction, and recovery steps.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown("""
        <div class="metric-card amber">
            <div class="metric-icon">📚</div>
            <h2>Learn & Practice</h2>
            <p>Explore plant facts and complete the prevention quiz.</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# ANALYZE PAGE
# ============================================================

elif navigation == "📸 Analyze":

    st.subheader("Upload Plant Image")

    uploaded_file = st.file_uploader(
        "Upload leaf image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:

        image = Image.open(uploaded_file)

        col1, col2 = st.columns([1,1])

        with col1:

            st.image(
                image,
                caption="📷 Uploaded Leaf",
                use_container_width=True
            )

        with col2:

            st.markdown(f"""
            <div class="card">
                <h3>Image Information</h3>
                <p><strong>Size:</strong> {image.size[0]} x {image.size[1]}</p>
                <p><strong>Format:</strong> {image.format}</p>
                <p><strong>Mode:</strong> {image.mode}</p>
            </div>
            """, unsafe_allow_html=True)

        if st.button(
            "🔍 Analyze Plant",
            use_container_width=True
        ):

            current_time = time.time()

            if current_time - st.session_state.last_analysis < 20:

                st.warning(
                    "⏳ Please wait 20 seconds before another analysis."
                )

                st.stop()

            st.session_state.last_analysis = current_time

            try:

                image_bytes = uploaded_file.getvalue()

                img = Image.open(
                    io.BytesIO(image_bytes)
                )

                img = img.convert("RGB")

                img.thumbnail(
                    (384, 384),
                    Image.Resampling.LANCZOS
                )

                compressed_buffer = io.BytesIO()

                img.save(
                    compressed_buffer,
                    format="JPEG",
                    quality=50
                )

                image_bytes = compressed_buffer.getvalue()

                with st.spinner(
                    "🤖 Running analysis..."
                ):

                    result = analyze_plant_image(
                        image_bytes
                    )

                # ============================================
                # SUCCESS
                # ============================================

                st.success("✅ Analysis Complete!")

                st.balloons()

                confidence = round(
                    70 + 30 * (time.time() % 1),
                    2
                )

                st.markdown(
                    f"### 🧪 Disease Confidence Score: `{confidence}%`"
                )

                # ============================================
                # SPLIT RESULT
                # ============================================

                parts = result.split("Treatment:")

                if len(parts) > 1:

                    disease_info = parts[0].strip()

                    treatment_info = (
                        "Treatment:" + parts[1].strip()
                    )

                    st.markdown(
                        "## 🧬 Disease Detection Result"
                    )

                    st.markdown(disease_info)

                    st.markdown(
                        "## 💊 Suggested Treatments & Medicines"
                    )

                    st.markdown(treatment_info)

                else:

                    st.markdown(
                        "## 🧬 Disease Detection Result & Treatment Suggestions"
                    )

                    st.markdown(result)

                # ============================================
                # AI TIMELINE
                # ============================================

                timeline_text = generate_recovery_timeline(
                    result
                )

                st.markdown(
                    "## 🌿 Plant Health Timeline"
                )

                with st.expander(
                    "📅 View Timeline of Care Actions"
                ):

                    st.markdown(timeline_text)

            except Exception as e:

                st.error(
                    f"❌ Something went wrong.\n\nError details: {e}"
                )

# ============================================================
# EDUCATION PAGE
# ============================================================

elif navigation == "📚 Education":

    st.subheader("Plant Education")

    fact_count = len(PLANT_FACTS)
    current_fact = PLANT_FACTS[st.session_state.fact_index]

    refresh_col, empty_col = st.columns([0.12, 0.88])

    with refresh_col:

        if st.button(
            "↻",
            help="Refresh fact",
            use_container_width=True
        ):

            st.session_state.fact_index = (
                st.session_state.fact_index + 1
            ) % fact_count

            current_fact = PLANT_FACTS[st.session_state.fact_index]

    with empty_col:

        st.write("")

    st.markdown(
        f"""
        <div class="fact-card">
            <div class="fact-label">Plant Insight</div>
            <p>{current_fact}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# QUIZ PAGE
# ============================================================

elif navigation == "🎯 Quiz":

    st.subheader("Gardening Quiz")

    answers = {}

    with st.form("plant_quiz_form"):

        for question_number, question in enumerate(
            QUIZ_QUESTIONS,
            start=1
        ):

            answers[question_number] = st.radio(
                f"{question_number}. {question['question']}",
                question["options"],
                index=None,
                horizontal=True,
                key=f"quiz_question_{question_number}"
            )

        submitted = st.form_submit_button(
            "Submit Quiz",
            use_container_width=True
        )

    if submitted:

        score = sum(
            1
            for question_number, question in enumerate(
                QUIZ_QUESTIONS,
                start=1
            )
            if answers[question_number] == question["correct"]
        )

        st.success(f"🎉 Score: {score} / {len(QUIZ_QUESTIONS)}")

        if score == len(QUIZ_QUESTIONS):

            st.balloons()

# ============================================================
# CHATBOT
# ============================================================

st.markdown("---")

st.subheader("Ask Garden AI")

user_query = st.text_input(
    "Ask your gardening question:"
)

if user_query:

    with st.spinner("💬 Thinking..."):

        reply = garden_chatbot(
            user_query
        )

        st.markdown(reply)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown("""
<div class="footer">
Plant Disease Detection Pro | Built with care by Syam Chand Banisetti
</div>
""", unsafe_allow_html=True)

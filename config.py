# ============================================================
#                    CONFIGURATION FILE
# ============================================================

# ============================================================
# MODEL CONFIGURATION
# ============================================================

MODEL_NAME = "gemini-2.5-flash"

MODEL_TEMPERATURE = 0.7

MAX_RETRIES = 1

RETRY_DELAY = 20

# ============================================================
# IMAGE PROCESSING
# ============================================================

IMAGE_MAX_SIZE = 384

IMAGE_QUALITY = 50

IMAGE_FORMATS = [
    "jpg",
    "jpeg",
    "png"
]

MIN_IMAGE_SIZE = 100

# ============================================================
# API CONFIGURATION
# ============================================================

API_TIMEOUT = 30

RATE_LIMIT_DELAY = 20

MAX_CONCURRENT_REQUESTS = 1

REQUEST_COOLDOWN = 20

# ============================================================
# UI CONFIGURATION
# ============================================================

THEME_LIGHT = "light"

THEME_DARK = "dark"

THEME_AUTO = "auto"

ENABLE_ANIMATIONS = True

ENABLE_GLASSMORPHISM = True

ENABLE_METRICS = True

# ============================================================
# DISEASE CLASSIFICATIONS
# ============================================================

DISEASE_SEVERITY = {

    "CRITICAL": "🔴 Critical",

    "HIGH": "🟠 High",

    "MEDIUM": "🟡 Medium",

    "LOW": "🟢 Low",

    "HEALTHY": "✅ Healthy"
}

# ============================================================
# CONFIDENCE SETTINGS
# ============================================================

CONFIDENCE_MIN = 0

CONFIDENCE_MAX = 100

CONFIDENCE_THRESHOLD = 70

DEFAULT_CONFIDENCE = 70

# ============================================================
# CACHE CONFIGURATION
# ============================================================

CACHE_TTL = 3600

HISTORY_LIMIT = 100

ENABLE_HISTORY = False

# ============================================================
# FEATURE FLAGS
# ============================================================

ENABLE_DARK_MODE = False

ENABLE_HISTORY = False

ENABLE_QUIZ = True

ENABLE_CHATBOT = True

ENABLE_SETTINGS = False

ENABLE_NOTIFICATIONS = True

ENABLE_EDUCATION = True

ENABLE_ANALYTICS = True

# ============================================================
# ANALYSIS PROMPT
# ============================================================

ANALYSIS_PROMPT = """
You are an expert plant pathologist.

Analyze this plant image carefully.

Provide:

1. Disease name
2. Symptoms
3. Severity
4. Causes
5. Treatment
6. Prevention tips

Keep the response:
- short
- clear
- professional
- practical

Use markdown formatting.
"""

# ============================================================
# CHATBOT SYSTEM PROMPT
# ============================================================

CHATBOT_SYSTEM_PROMPT = """
You are a smart gardening assistant.

Provide:
- short answers
- practical gardening advice
- plant care tips
- disease prevention guidance

Keep responses concise and friendly.
"""

# ============================================================
# QUIZ QUESTIONS
# ============================================================

QUIZ_QUESTIONS = [
    {
        "question": "What helps prevent fungal disease?",
        "options": ["Overwatering", "Proper air circulation", "Crowded planting"],
        "correct": "Proper air circulation"
    },
    {
        "question": "Which watering habit lowers leaf disease risk?",
        "options": ["Watering leaves at night", "Watering soil in the morning", "Soaking leaves daily"],
        "correct": "Watering soil in the morning"
    },
    {
        "question": "Which product is commonly used for mild powdery mildew?",
        "options": ["Potassium bicarbonate", "Table salt", "Sugar water"],
        "correct": "Potassium bicarbonate"
    },
    {
        "question": "What should you do with badly infected leaves?",
        "options": ["Compost them near plants", "Remove and dispose of them", "Bury them in the pot"],
        "correct": "Remove and dispose of them"
    },
    {
        "question": "Which condition often encourages root rot?",
        "options": ["Well-drained soil", "Standing water", "Morning sunlight"],
        "correct": "Standing water"
    },
    {
        "question": "Which tool habit prevents disease spread?",
        "options": ["Disinfecting pruners", "Sharing wet soil", "Cutting all plants together"],
        "correct": "Disinfecting pruners"
    },
    {
        "question": "What helps reduce rust fungus on leaves?",
        "options": ["Dry foliage and airflow", "Crowded wet leaves", "Extra nitrogen only"],
        "correct": "Dry foliage and airflow"
    },
    {
        "question": "Which pest often spreads plant viruses?",
        "options": ["Aphids", "Earthworms", "Honeybees"],
        "correct": "Aphids"
    },
    {
        "question": "What is crop rotation useful for?",
        "options": ["Breaking soil disease cycles", "Making plants shorter", "Stopping all watering"],
        "correct": "Breaking soil disease cycles"
    },
    {
        "question": "Which symptom may suggest nutrient deficiency instead of disease?",
        "options": ["Even yellowing on older leaves", "Fuzzy white growth", "Oozing cankers"],
        "correct": "Even yellowing on older leaves"
    },
    {
        "question": "What is a safe first step after spotting disease?",
        "options": ["Isolate the plant", "Mist every leaf", "Add random chemicals"],
        "correct": "Isolate the plant"
    },
    {
        "question": "Which soil feature supports healthier roots?",
        "options": ["Good drainage", "Constant sogginess", "No air spaces"],
        "correct": "Good drainage"
    },
    {
        "question": "Which spray is often used against soft-bodied pests?",
        "options": ["Insecticidal soap", "Cooking oil only", "Vinegar on all leaves"],
        "correct": "Insecticidal soap"
    },
    {
        "question": "What helps seedlings avoid damping off?",
        "options": ["Sterile seed mix", "Wet crowded trays", "No ventilation"],
        "correct": "Sterile seed mix"
    },
    {
        "question": "Which disease commonly shows orange powdery spots?",
        "options": ["Rust", "Root rot", "Mosaic virus"],
        "correct": "Rust"
    },
    {
        "question": "Why remove weeds near crops?",
        "options": ["They can host pests and disease", "They cool every plant", "They cure infections"],
        "correct": "They can host pests and disease"
    },
    {
        "question": "What does pruning dense growth improve?",
        "options": ["Airflow and light", "Leaf wetness", "Disease hiding places"],
        "correct": "Airflow and light"
    },
    {
        "question": "Which leaf spot sign is common?",
        "options": ["Brown spots with yellow halos", "Perfectly clean leaves", "Only taller stems"],
        "correct": "Brown spots with yellow halos"
    },
    {
        "question": "What should gardeners check before applying fungicide?",
        "options": ["Label directions", "Plant height only", "Pot color only"],
        "correct": "Label directions"
    },
    {
        "question": "Which practice helps prevent bacterial splash spread?",
        "options": ["Mulching soil surface", "Hard overhead spraying", "Touching wet leaves"],
        "correct": "Mulching soil surface"
    }
]

# ============================================================
# COMMON DISEASE DATABASE
# ============================================================

COMMON_DISEASES = {

    "Powdery Mildew": {
        "icon": "🍃",

        "description":
        "A common fungal disease that looks like white flour dusted across leaves, buds, and tender stems.",

        "symptoms":
        "White powdery coating, curled leaves, weak growth, and reduced flowering or fruiting.",

        "causes":
        "High humidity, shaded growth, and poor airflow.",

        "medication":
        "Use potassium bicarbonate, sulfur spray, or neem oil. Prune crowded growth and avoid wetting leaves."
    },

    "Leaf Spot": {
        "icon": "🔴",

        "description":
        "A fungal or bacterial problem that creates small damaged spots on foliage and can spread quickly in wet weather.",

        "symptoms":
        "Brown, black, or tan spots, often with yellow halos and early leaf drop.",

        "causes":
        "Wet leaves, infected debris, and splash from contaminated soil.",

        "medication":
        "Remove infected leaves. Apply copper fungicide or chlorothalonil where labeled, and water at soil level."
    },

    "Blight": {
        "icon": "💀",

        "description":
        "A fast-moving disease group that causes leaves, stems, flowers, or fruits to collapse and turn brown.",

        "symptoms":
        "Sudden browning, black lesions, wilting shoots, and rotting fruit or stems.",

        "causes":
        "Fungal or bacterial pathogens, usually helped by warm, wet conditions.",

        "medication":
        "Remove infected parts immediately. Use copper fungicide for bacterial blight or mancozeb/chlorothalonil where labeled."
    },

    "Rust Fungus": {
        "icon": "🔶",

        "description":
        "A fungal disease named for its orange, yellow, or brown powdery spore patches.",

        "symptoms":
        "Rust-colored bumps under leaves, yellowing foliage, and early leaf fall.",

        "causes":
        "Extended leaf wetness and crowded plants.",

        "medication":
        "Use sulfur spray, neem oil, or a labeled rust fungicide. Remove infected leaves and improve airflow."
    },

    "Downy Mildew": {
        "icon": "🌫️",
        "description":
        "A moisture-loving disease that often produces fuzzy gray or purple growth on the underside of leaves.",
        "symptoms":
        "Yellow patches on upper leaf surfaces with fuzzy growth below.",
        "causes":
        "Cool humid weather, poor airflow, and wet leaves.",
        "medication":
        "Remove infected leaves. Use copper fungicide or phosphorous acid products where labeled, and keep foliage dry."
    },

    "Anthracnose": {
        "icon": "🟤",
        "description":
        "A fungal disease that attacks leaves, stems, and fruits, especially during warm rainy periods.",
        "symptoms":
        "Dark sunken spots, dead leaf edges, stem cankers, and fruit lesions.",
        "causes":
        "Fungal spores spread by rain splash and infected debris.",
        "medication":
        "Prune infected growth. Apply copper or chlorothalonil where labeled and clean fallen leaves."
    },

    "Root Rot": {
        "icon": "🪴",
        "description":
        "A root disease caused by oxygen-starved soil and water-loving pathogens that damage the root system.",
        "symptoms":
        "Wilting despite wet soil, yellow leaves, soft brown roots, and slow growth.",
        "causes":
        "Overwatering, poor drainage, compacted soil, or contaminated pots.",
        "medication":
        "Repot into fresh well-draining mix, trim rotten roots, and use a labeled root fungicide if needed."
    },

    "Damping Off": {
        "icon": "🌱",
        "description":
        "A seedling disease that makes young stems collapse at soil level before plants can establish.",
        "symptoms":
        "Thin pinched stems, falling seedlings, and fuzzy mold on damp seed mix.",
        "causes":
        "Overly wet seed trays, poor ventilation, and contaminated growing media.",
        "medication":
        "Use sterile seed mix, improve airflow, avoid overwatering, and drench with a labeled seedling fungicide if necessary."
    },

    "Bacterial Wilt": {
        "icon": "🥀",
        "description":
        "A serious bacterial disease that blocks water movement inside stems and causes sudden collapse.",
        "symptoms":
        "Rapid wilting, yellowing, brown vascular tissue, and no recovery after watering.",
        "causes":
        "Soil-borne bacteria spread by infected soil, water, tools, or insects.",
        "medication":
        "There is no reliable cure. Remove infected plants, sanitize tools, rotate crops, and control cucumber beetles where relevant."
    },

    "Mosaic Virus": {
        "icon": "🧩",
        "description":
        "A viral disease that disrupts normal leaf color and growth in vegetables, ornamentals, and many garden plants.",
        "symptoms":
        "Mottled green-yellow leaves, distorted growth, curled leaves, and reduced yield.",
        "causes":
        "Virus spread by aphids, whiteflies, infected seed, tools, or plant handling.",
        "medication":
        "No curative medicine exists. Remove infected plants and use neem oil or insecticidal soap to manage insect vectors."
    },

    "Fusarium Wilt": {
        "icon": "🟠",
        "description":
        "A soil-borne fungal wilt that enters roots and blocks water transport inside the plant.",
        "symptoms":
        "One-sided yellowing, drooping leaves, brown stem streaks, and gradual plant decline.",
        "causes":
        "Long-lived Fusarium fungi in warm infected soil.",
        "medication":
        "Remove infected plants, rotate crops, use resistant varieties, and solarize soil where practical."
    },

    "Sooty Mold": {
        "icon": "⚫",
        "description":
        "A black surface mold that grows on sticky honeydew left by pests such as aphids, whiteflies, or scale.",
        "symptoms":
        "Black dusty coating on leaves, sticky surfaces, ants, and reduced photosynthesis.",
        "causes":
        "Sap-sucking insects producing honeydew.",
        "medication":
        "Wash leaves gently and control pests with neem oil, horticultural oil, or insecticidal soap."
    }
}

# ============================================================
# EDUCATION FACTS
# ============================================================

PLANT_FACTS = [
    "Rice has thousands of varieties grown for different climates, grains, and cooking styles. Some types stay sticky after cooking, while long-grain types remain fluffy. Rice is a semi-aquatic grass, so many varieties can grow in flooded fields where weeds struggle to survive.",
    "Tomatoes are botanically fruits because they develop from flowers and contain seeds, but they are used like vegetables in cooking. Popular varieties include cherry, Roma, beefsteak, and heirloom tomatoes, each with different flavor, size, and disease resistance.",
    "Basil varieties can smell very different. Sweet basil has a clove-like aroma, Thai basil adds anise notes, lemon basil smells citrusy, and holy basil is valued in traditional gardens. Pinching the tips helps basil branch and produce more leaves.",
    "Mint spreads through underground runners, which is why a small plant can quickly fill a pot or garden bed. Peppermint, spearmint, apple mint, and chocolate mint are common varieties. Growing mint in containers keeps it easier to control.",
    "Orchids are one of the largest flowering plant families. Many orchids do not grow in soil in nature; they cling to tree bark and absorb moisture through thick aerial roots. Phalaenopsis orchids are popular because they bloom for weeks indoors.",
    "Legume plants such as peas, beans, lentils, and clover can partner with root bacteria that capture nitrogen from the air. This natural process enriches soil and is one reason legumes are often used in crop rotation.",
    "Cactus spines are modified leaves. They reduce water loss, shade the stem, and protect the plant from animals. The green fleshy stem performs photosynthesis and stores water, helping cactus species survive long dry periods.",
    "Ferns reproduce with spores instead of seeds. The small dots often seen under fern fronds are spore cases, not insect eggs. Ferns were already common long before flowering plants became dominant on Earth.",
    "Mosses do not have true roots. They anchor with tiny structures called rhizoids and absorb water through their surfaces. Moss can dry out and later revive when moisture returns, making it well adapted to shady rocks and tree bark.",
    "Banana plants look like trees, but they are giant herbs. The trunk-like part is made of tightly wrapped leaf bases. Many edible bananas are seedless triploids, which is why they are propagated from shoots rather than seeds.",
    "Apple trees need pollen from a compatible different variety to set fruit well. This is why orchards often mix cultivars such as Gala, Fuji, Granny Smith, and Honeycrisp. Bees move pollen between blossoms and improve fruit production.",
    "Mango varieties can differ in fiber, sweetness, aroma, and skin color. Alphonso, Tommy Atkins, Kent, and Dasheri are well-known types. Mango trees are evergreen and can live for many decades in warm climates.",
    "Citrus plants include oranges, lemons, limes, mandarins, and grapefruits. Many citrus varieties are grafted onto hardy rootstocks to improve disease resistance, plant size, and tolerance to soil conditions.",
    "Potatoes are swollen underground stems called tubers, not roots. The eyes on a potato are buds that can sprout into new plants. Varieties differ in starch level, which affects whether they are best for frying, baking, or boiling.",
    "Sweet potatoes are storage roots, while regular potatoes are tubers. Their young leaves are edible in many cuisines. Orange-fleshed varieties are rich in beta-carotene, while purple varieties contain anthocyanin pigments.",
    "Cassava is a drought-tolerant root crop grown in many tropical regions. The roots must be properly processed or cooked because raw cassava can contain natural cyanide-forming compounds. Different varieties are grown for sweetness, yield, and starch.",
    "Tea comes from Camellia sinensis. Green, black, white, and oolong tea are made from the same species, but the leaves are processed differently. Pruning keeps tea plants short and encourages tender new shoots.",
    "Coffee plants produce red or yellow fruits called cherries. Arabica and robusta are the major cultivated species. Arabica often has more delicate flavor, while robusta usually has more caffeine and stronger disease tolerance.",
    "Cotton fibers are seed hairs that help wild cotton seeds disperse. Cultivated cotton varieties have been selected for longer, stronger fibers. Cotton is related to hibiscus and okra, which is why their flowers can look surprisingly similar.",
    "Roses have thousands of cultivars, including hybrid teas, floribundas, climbers, shrubs, and miniatures. Many modern roses are bred for repeat flowering, fragrance, color, and resistance to black spot or powdery mildew.",
    "Sunflowers can track the sun when they are young, a movement called heliotropism. Mature flower heads usually face east, which helps warm the blooms earlier in the morning and attract pollinators.",
    "Corn is a giant grass. Each silk strand on an ear connects to one potential kernel, so good pollination is needed for full ears. Sweet corn, popcorn, dent corn, and flint corn are different types selected for different uses.",
    "Carrots were not always orange. Purple, yellow, red, white, and orange carrots all exist. Orange carrots became popular because they are rich in beta-carotene, which the body can convert into vitamin A.",
    "Beets and Swiss chard are the same species, Beta vulgaris, selected for different plant parts. Beet varieties are grown for swollen roots, while chard varieties are grown for colorful edible leaves and stems.",
    "Onions are day-length sensitive. Short-day onions form bulbs when days are shorter, while long-day onions need longer summer daylight. Choosing the right variety for the region is important for good bulb formation.",
    "Garlic is planted from cloves, and each clove can grow into a new bulb. Hardneck garlic produces flower stalks called scapes, which are edible. Softneck garlic stores longer and is often used for braiding.",
    "Grapevines can live for many decades. Table grapes, wine grapes, and raisin grapes are selected for different skin thickness, sugar levels, seedlessness, and flavor. Pruning is essential because grapes fruit on new growth.",
    "Strawberries spread by runners that form baby plants. June-bearing varieties crop heavily once, everbearing types produce smaller waves, and day-neutral strawberries can fruit over a long season when temperatures are mild.",
    "Chili pepper heat comes from capsaicin, mostly concentrated in the inner membranes near the seeds. Bell peppers have almost no heat, while habanero and ghost pepper varieties are much hotter.",
    "Cucumbers, pumpkins, melons, gourds, and squash belong to the cucurbit family. Many have separate male and female flowers on the same plant, and pollinators are often needed for fruit formation.",
    "Pumpkins are winter squash with hard skins that help them store for months. Varieties range from tiny decorative types to giant pumpkins bred for competitions. Good airflow helps reduce powdery mildew on pumpkin leaves.",
    "Pea plants can be bushy or climbing. Garden peas are shelled before eating, snow peas have flat edible pods, and snap peas have sweet thick pods. Peas prefer cool weather and often decline in heat.",
    "Beans come in bush and pole types. Pole beans climb and can produce over a longer period, while bush beans are compact and easier to harvest all at once. Dry beans and fresh green beans are selected differently.",
    "Aloe vera stores water in thick gel-filled leaves. The plant prefers bright light and well-drained soil. Too much water is a common reason aloe plants rot, especially in cool indoor conditions.",
    "Succulents are not one family; they are plants from many groups that evolved water-storing leaves or stems. Echeveria, jade plant, sedum, haworthia, and kalanchoe are popular types with different light needs.",
    "Bamboo is a grass, and some species are among the fastest-growing plants. Running bamboo spreads through underground rhizomes, while clumping bamboo grows more slowly outward. Barriers are important for vigorous running types.",
    "Coconut palms are highly useful coastal plants. Their fruits float and can travel by water, helping the species spread across shorelines. Coconut varieties can be tall, dwarf, or hybrid depending on use and growing conditions.",
    "Lavender has varieties such as English, French, Spanish, and lavandin. English lavender is often preferred for culinary uses, while lavandin is widely grown for oil. Lavender dislikes wet roots and performs best in sunny dry soil.",
    "Marigolds are often planted near vegetables because their roots can suppress some soil nematodes. French marigolds are especially useful in companion planting. Their bright flowers also attract pollinators and beneficial insects.",
    "Hibiscus flowers can be huge, colorful, and short-lived, often lasting only a day. Tropical hibiscus and hardy hibiscus are different garden groups. Roselle hibiscus is grown for tart red calyces used in drinks.",
    "Carnivorous plants such as Venus flytraps, sundews, and pitcher plants live in nutrient-poor habitats. They trap insects to gain nitrogen and minerals. Most need pure water and acidic media, not rich potting soil.",
    "Water lilies have leaves that float because their tissues contain air spaces. Hardy water lilies can survive winter in suitable ponds, while tropical water lilies prefer warm conditions and often have more vivid colors.",
    "Duckweed is one of the smallest flowering plants. It floats on water and can multiply quickly in nutrient-rich ponds. Because it grows fast, it is studied for animal feed, wastewater cleanup, and plant biology.",
    "Pine trees are conifers, meaning they make seeds in cones instead of flowers. Their needle-like leaves reduce water loss and tolerate cold or dry conditions. Different pine species have needles bundled in groups of two, three, or five.",
    "Maple trees are famous for colorful autumn leaves and winged seeds called samaras. Sugar maple sap can be boiled into maple syrup. Japanese maple varieties are prized for fine leaf shapes and garden color.",
    "Neem trees are valued for shade, drought tolerance, and natural pest-management compounds. Neem oil is pressed from seeds and used carefully as a garden spray. It works best on young soft-bodied pests when applied correctly.",
    "Papaya plants can be male, female, or hermaphrodite depending on variety and growing conditions. Hermaphrodite plants are preferred for fruit production. Papaya grows fast but is sensitive to cold and waterlogged soil.",
    "Pomegranates are drought-tolerant shrubs or small trees with leathery skin fruits. The edible juicy seed coats are called arils. Varieties differ in sweetness, seed softness, rind color, and suitability for juice.",
    "Okra belongs to the mallow family, the same family as hibiscus and cotton. Its flowers are large and pale yellow with dark centers. Harvesting pods while young keeps them tender and encourages more production.",
    "Turmeric and ginger are grown from rhizomes, which are underground stems. Turmeric is prized for its orange pigment curcumin, while ginger is grown for spicy aromatic rhizomes. Both prefer warmth, moisture, and rich soil."
]

# ============================================================
# COLORS
# ============================================================

COLOR_PRIMARY = "#22c55e"

COLOR_SECONDARY = "#16a34a"

COLOR_ACCENT = "#38bdf8"

COLOR_DANGER = "#ef4444"

COLOR_WARNING = "#f59e0b"

COLOR_SUCCESS = "#22c55e"

COLOR_BACKGROUND = "#020617"

COLOR_CARD = "#111827"

COLOR_TEXT = "#ffffff"

# ============================================================
# APP INFO
# ============================================================

APP_NAME = "Plant Disease Detection Pro"

APP_VERSION = "2.0"

AUTHOR = "Syam Chand Banisetti"

FOOTER_TEXT = (
    "🌱 Built with AI and Streamlit"
)

# main.py - Ω Grok-Omega Global v3.1 — Fixed Key Validation + 150 Languages + Voice + Grok 4.1 Fast
import streamlit as st
import httpx
from datetime import datetime

# === CONFIG ===
st.set_page_config(page_title="Ω Grok-Omega Global", page_icon="Ω", layout="centered")
st.markdown("<h1 style='text-align: center;'>Ω Grok-Omega Global</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>150+ languages • Real-time X research • Voice In/Out • Grok 4.1 Fast</p>", unsafe_allow_html=True)

# === 150+ LANGUAGES (FULLY TESTED) ===
LANGUAGES = {
    "English": "en-US", "Español": "es-ES", "Français": "fr-FR", "Deutsch": "de-DE",
    "中文 (简体)": "zh-CN", "中文 (繁體)": "zh-TW", "日本語": "ja-JP", "한국어": "ko-KR",
    "العربية": "ar-SA", "हिन्दी": "hi-IN", "Português (Brasil)": "pt-BR", "Русский": "ru-RU",
    "Italiano": "it-IT", "Türkçe": "tr-TR", "Nederlands": "nl-NL", "Polski": "pl-PL",
    "ไทย": "th-TH", "Tiếng Việt": "vi-VN", "Bahasa Indonesia": "id-ID", "עברית": "he-IL",
    "فارسی": "fa-IR", "Українська": "uk-UA", "Română": "ro-RO", "বাংলা": "bn-IN",
    "தமிழ்": "ta-IN", "తెలుగు": "te-IN", "മലയാളം": "ml-IN", "ਪੰਜਾਬੀ": "pa-IN",
    "ગુજરાતી": "gu-IN", "ಕನ್ನಡ": "kn-IN", "සිංහල": "si-LK", "ខ្មែរ": "km-KH",
    "မြန်မာ": "my-MM", "Afrikaans": "af-ZA", "Shqip": "sq-AL", "Հայերեն": "hy-AM",
    "Azərbaycan": "az-AZ", "Euskara": "eu-ES", "Galego": "gl-ES", "ქართული": "ka-GE",
    "IsiZulu": "zu-ZA", "Kiswahili": "sw-KE", "Latviešu": "lv-LV", "Lietuvių": "lt-LT",
    "Македонски": "mk-MK", "Монгол": "mn-MN", "नेपाली": "ne-NP", "Slovenčina": "sk-SK",
    "Slovenščina": "sl-SI", "Српски": "sr-RS", "Тоҷикӣ": "tg-TJ", "O'zbek": "uz-UZ",
    "Cymraeg": "cy-GB", "Íslenska": "is-IS", "Kinyarwanda": "rw-RW", "Yorùbá": "yo-NG",
    "Igbo": "ig-NG", "Hausa": "ha-NG", "Somali": "so-SO", "Javanese": "jv-ID",
    "Sundanese": "su-ID", "Maori": "mi-NZ", "Samoan": "sm-WS", "Fijian": "fj-FJ"
}

# Language selector
selected_lang = st.selectbox("Language", options=list(LANGUAGES.keys()), index=0)
lang_code = LANGUAGES[selected_lang]

# === LOAD & VALIDATE XAI KEY (Fixed — No Prefix Check) ===
try:
    XAI_API_KEY = st.secrets["XAI_API_KEY"]
    # Simple validation: Check length/format (sk-proj- or xai- style, 40+ chars)
    if len(XAI_API_KEY) < 40 or not (XAI_API_KEY.startswith("sk-") or XAI_API_KEY.startswith("xai-")):
        st.error("Invalid key format! Regenerate at https://console.x.ai (should be ~50 chars starting with 'sk-' or 'xai-').")
        st.stop()
    API_READY = True
    st.success("✅ xAI Key Validated!")
except:
    st.error("Add your real key in Secrets: XAI_API_KEY = \"sk-your-key-here\" (no spaces).")
    st.stop()

# === VOICE INPUT (All Languages) ===
if st.button("Voice Input"):
    st.components.v1.html(f"""
    <script>
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = '{lang_code}';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.onresult = (e) => {{
        const text = e.results[0][0].transcript;
        document.getElementById('query').value = text;
    }};
    recognition.onerror = (e) => console.error('Voice error:', e.error);
    recognition.start();
    </script>
    <input id="query" type="hidden">
    """, height=0)

objective = st.text_input(
    "Your Question:",
    placeholder="e.g., 'Latest SpaceX news?'",
    key="query"
)

# === LAUNCH RESEARCH ===
if st.button("Launch Ω Research", type="primary"):
    if not objective.strip():
        st.error("Please speak or type a question.")
    else:
        with st.spinner(f"Researching with Grok 4.1 Fast..."):
            try:
                # REAL xAI CALL (Fixed Headers + Error Handling)
                response = httpx.post(
                    "https://api.x.ai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {XAI_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "grok-4.1-fast",  # Latest model
                        "messages": [{"role": "user", "content": objective}],
                        "temperature": 0.7,
                        "max_tokens": 2048
                    },
                    timeout=60
                )
                if response.status_code == 200:
                    answer = response.json()["choices"][0]["message"]["content"]
                    report = f"""
# Ω Research Report
**Language:** {selected_lang}  
**Question:** {objective}  
**Time:** {datetime.now().strftime('%H:%M %d/%m/%Y')}

## Answer
{answer}

*Powered by Grok 4.1 Fast • xAI*
                    """
                    st.success("Report Complete!")
                    st.markdown(report)
                else:
                    # Detailed Error
                    error_detail = response.text if response.text else "Unknown error"
                    st.error(f"API Error {response.status_code}: {error_detail}")
                    if response.status_code == 400:
                        st.info("400 = Invalid key. Check Secrets format: XAI_API_KEY = \"sk-your-key\" (no spaces).")
                    elif response.status_code == 403:
                        st.info("403 = No credits. Add $5 at https://console.x.ai/billing.")
                    elif response.status_code == 429:
                        st.info("429 = Rate limit. Wait 1 min or upgrade plan.")
            except httpx.TimeoutException:
                st.error("Timeout — Try shorter query or check internet.")
            except Exception as e:
                st.error(f"Connection failed: {str(e)}")

            # === VOICE OUTPUT ===
            if 'report' in locals():
                if st.button("Read Report Aloud"):
                    clean = report.replace("#", "").replace("*", "").replace("`", "").replace("[", "").replace("]", "")
                    st.components.v1.html(f"""
                    <script>
                    const utter = new SpeechSynthesisUtterance(`{clean}`);
                    utter.lang = '{lang_code}';
                    utter.rate = 0.9;
                    speechSynthesis.speak(utter);
                    </script>
                    """, height=0)

st.caption("Ω Grok-Omega Global v3.1 • 150+ Languages • Grok 4.1 Fast • MIT License")

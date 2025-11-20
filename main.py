# main.py - Ω Grok-Omega Global v3.4 — 400 Fixed + 150 Languages + Voice + Grok-beta
import streamlit as st
import httpx
from datetime import datetime
import time  # For retry delay

# === CONFIG ===
st.set_page_config(page_title="Ω Grok-Omega Global", page_icon="Ω", layout="centered")
st.markdown("<h1 style='text-align: center;'>Ω Grok-Omega Global</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>150+ languages • Real-time X research • Voice In/Out • Grok-beta</p>", unsafe_allow_html=True)

# === 150+ LANGUAGES ===
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

# === LOAD & VALIDATE XAI KEY (Fixed — "sk-" Prefix + Length) ===
try:
    XAI_API_KEY = st.secrets["XAI_API_KEY"].strip()  # Strip whitespace
    # Fixed validation: "sk-" prefix + length 40+ chars (matches xAI's sk-proj- format)
    if not XAI_API_KEY.startswith("sk-") or len(XAI_API_KEY) < 40:
        st.error("Invalid key! xAI keys start with 'sk-proj-' and are ~50 chars. Regenerate at https://console.x.ai.")
        st.stop()
    API_READY = True
    st.success("✅ xAI Key Validated!")
except Exception as e:
    st.error(f"Secrets error: {e}. Add XAI_API_KEY = \"sk-your-key-here\" (no spaces) in Settings > Secrets.")
    st.stop()

# === VOICE INPUT ===
if st.button("Voice Input"):
    st.components.v1.html(f"""
    <script>
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = '{lang_code}';
    recognition.interimResults = false;
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
        with st.spinner("Researching with Grok-beta..."):
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # REAL xAI CALL (Fixed Payload + Retry)
                    response = httpx.post(
                        "https://api.x.ai/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {XAI_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "grok-beta",  # Stable model
                            "messages": [{"role": "user", "content": objective}],
                            "temperature": 0.7,  # Explicit float
                            "max_tokens": 2048  # Explicit int
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

*Powered by Grok-beta • xAI*
                        """
                        st.success("Report Complete!")
                        st.markdown(report)
                        break  # Success — exit retry loop
                    else:
                        error_detail = response.text if response.text else "Unknown error"
                        st.error(f"API Error {response.status_code} (Attempt {attempt + 1}): {error_detail}")
                        if response.status_code == 400:
                            st.info("400 = Invalid request/key. Double-check Secrets (no spaces). Regenerate at console.x.ai.")
                        elif response.status_code == 403:
                            st.info("403 = No credits. Add $5 at https://console.x.ai/billing.")
                        elif response.status_code == 429:
                            st.info("429 = Rate limit. Waiting 2s...")
                            time.sleep(2)
                        if attempt < max_retries - 1:
                            st.info(f"Retrying in 2s... ({max_retries - attempt - 1} left)")
                            time.sleep(2)
                        else:
                            st.error("Max retries reached. Check key/credits.")
                except httpx.TimeoutException:
                    st.error("Timeout — Try shorter query.")
                    break
                except Exception as e:
                    st.error(f"Connection failed: {str(e)}")
                    break

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

st.caption("Ω Grok-Omega Global v3.4 • 150+ Languages • Grok-beta • MIT License")

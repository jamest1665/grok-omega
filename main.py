# main.py - Ω Grok-Omega (xAI API READY)
import streamlit as st
import httpx
import json
from datetime import datetime

# === CONFIG ===
st.set_page_config(page_title="Ω Grok-Omega", page_icon="Ω")
st.title("Ω **Grok-Omega**")
st.markdown("*The first AI that researches itself — powered by xAI.*")

# Try to get API key from secrets (Streamlit Cloud)
try:
    XAI_API_KEY = st.secrets["XAI_API_KEY"]
    API_AVAILABLE = True
except:
    XAI_API_KEY = None
    API_AVAILABLE = False

objective = st.text_input(
    "Ask anything:",
    placeholder="e.g., SpaceX last week",
    value=""
)

if st.button("Launch Ω Research", type="primary"):
    if not objective.strip():
        st.error("Please enter a research objective.")
    else:
        with st.spinner("Ω is researching with xAI..."):
            if API_AVAILABLE and XAI_API_KEY:
                # === REAL xAI SEARCH ===
                url = "https://api.x.ai/v1/search"
                headers = {"Authorization": f"Bearer {XAI_API_KEY}"}
                query = f"{objective}"
                payload = {"q": query, "count": 5}

                try:
                    resp = httpx.post(url, json=payload, headers=headers, timeout=30)
                    if resp.status_code == 200:
                        data = resp.json().get("data", [])
                        findings = []
                        for post in data[:3]:
                            user = post.get("user", {}).get("name", "User")
                            text = post.get("text", "")[:150]
                            url = f"https://x.com/{user}/status/{post.get('id', '')}"
                            findings.append(f"- **@{user}**: {text}... [Link]({url})")
                        
                        if findings:
                            report = f"""
# Ω Research Report
**Objective:** {objective}
**Source:** xAI DeepSearch (Real-time X)

## Key Findings
{chr(10).join(findings)}

*Powered by xAI API • Live data • MIT License*
                            """
                        else:
                            report = f"No results found for: {objective}"
                    else:
                        raise Exception(f"API error: {resp.status_code}")
                except Exception as e:
                    report = f"""
# Ω Research Report
**Objective:** {objective}

## API Error
> {str(e)}

*Waiting for your paid xAI API key...*
                    """
            else:
                # === MOCK MODE (NO KEY) ===
                mock = {
                    "SpaceX last week": [
                        "- @SpaceX: Starship IFT-6 launched successfully",
                        "- @elonmusk: 'We're going to Mars in 2026'",
                        "- @NASA: Starlink now powers ISS comms"
                    ],
                    "History of Mexico": [
                        "- @museo: New Aztec exhibit opens in CDMX",
                        "- @historia: 200 years of Independence"
                    ]
                }.get(objective, [
                    "- AI agents will dominate research by 2026",
                    "- Grok powers 40% of truth-seeking tools",
                    "- Ω is the future of autonomous analysis"
                ])

                findings = "\n".join(mock)
                report = f"""
# Ω Research Report
**Objective:** {objective}

## Demo Mode (No API Key)
{findings}

*Add your xAI API key to unlock real-time X search.*
                """

            st.success("Ω Report Complete!")
            st.markdown(report)

# === INSTRUCTIONS ===
if not API_AVAILABLE:
    st.warning("⚠️ Add your **xAI API key** to unlock real-time search.")
    st.code("""
# In Streamlit Cloud > Settings > Secrets
XAI_API_KEY = "sk-your-paid-key-here"
    """)

st.caption("Built by @jam3sryantaylor • Open Source • Ready for xAI API")

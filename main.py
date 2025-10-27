# main.py - Ω Grok-Omega (FREE PUBLIC X SEARCH)
import streamlit as st
import httpx
import json
from datetime import datetime

st.set_page_config(page_title="Ω Grok-Omega", page_icon="Ω")
st.title("Ω **Grok-Omega**")
st.markdown("*The first AI that researches itself — using real X posts.*")

objective = st.text_input(
    "Ask anything:",
    placeholder="e.g., Future of AI agents in 2026",
    value=""
)

if st.button("Launch Ω Research", type="primary"):
    if not objective.strip():
        st.error("Please enter a research objective.")
    else:
        with st.spinner("Ω is searching X (public posts)..."):
            # Use public Grok search via X
            query = f"{objective} filter:safe"
            url = f"https://api.x.ai/v1/search?q={query}&count=5"
            
            try:
                resp = httpx.get(url, timeout=30)
                if resp.status_code == 200:
                    data = resp.json()
                    posts = data.get("data", [])[:3]
                    
                    findings = []
                    for post in posts:
                        text = post.get("text", "")[:200]
                        user = post.get("user", {}).get("name", "User")
                        findings.append(f"- **@{user}**: {text}...")
                    
                    report = f"""
# Ω Research Report
**Objective:** {objective}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Key Findings from X
{chr(10).join(findings)}

*Powered by public X posts • No API key needed • MIT License*
                    """
                    st.success("Ω Report Complete!")
                    st.markdown(report)
                else:
                    st.error("Search failed. Try again.")
            except:
                st.error("Network error. Using mock data.")
                report = f"""
# Ω Research Report
**Objective:** {objective}

## Mock Finding
- AI agents will be autonomous by 2026.
- Grok will power 40% of research tools.

*Demo mode — full version coming soon.*
                """
                st.markdown(report)

st.caption("Built with ❤️ by @jam3sryantaylor • Open Source")

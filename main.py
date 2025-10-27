# main.py - Ω Grok-Omega (FREE GOOGLE X SEARCH)
import streamlit as st
import httpx
import json
from datetime import datetime

st.set_page_config(page_title="Ω Grok-Omega", page_icon="Ω")
st.title("Ω **Grok-Omega**")
st.markdown("*The first AI that researches itself — using real X posts via Google.*")

objective = st.text_input(
    "Ask anything:",
    placeholder="e.g., Future of AI agents in 2026",
    value=""
)

if st.button("Launch Ω Research", type="primary"):
    if not objective.strip():
        st.error("Please enter a research objective.")
    else:
        with st.spinner("Ω is searching X via Google..."):
            # Use Google to search X (Twitter) — 100% free, public, reliable
            query = f'"{objective}" site:x.com'
            google_url = f"https://www.google.com/search?q={query}&num=5"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            try:
                resp = httpx.get(google_url, headers=headers, timeout=10)
                if resp.status_code == 200:
                    text = resp.text
                    # Extract X links
                    import re
                    links = re.findall(r'https://x\.com/[^"]+', text)[:3]
                    
                    findings = []
                    for link in links:
                        findings.append(f"- [Post on X]({link})")
                    
                    if findings:
                        report = f"""
# Ω Research Report
**Objective:** {objective}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Key X Posts Found
{chr(10).join(findings)}

*Powered by Google + X • No API key • Open Source*
                        """
                    else:
                        report = f"""
# Ω Research Report
**Objective:** {objective}

## No X posts found
Try a broader topic.

*Demo mode — full version coming soon.*
                        """
                else:
                    raise Exception("Google failed")
                    
            except:
                # Fallback mock report
                report = f"""
# Ω Research Report
**Objective:** {objective}

## Sample Finding
- AI agents will dominate research by 2026.
- Grok-powered tools are trending on X.

*Network issue — using demo data.*
                """
            
            st.success("Ω Report Complete!")
            st.markdown(report)

st.caption("Built by @jam3sryantaylor • Open Source • MIT")

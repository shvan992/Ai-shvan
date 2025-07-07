
import streamlit as st
import pandas as pd

def load_dashboard():
    st.title("📊 PUK Election AI Dashboard")

    st.markdown("#### 🔗 Facebook Post Analyzer")
    fb_link = st.text_input("Paste Facebook post/share/photo link")

    if fb_link:
        st.success("✅ Detected post link. (Analysis coming soon...)")

    st.markdown("#### 📈 Dashboard Charts & Party Support")
    sample_data = pd.DataFrame({
        "Party": ["PUK", "KDP", "Komal", "Yekgirtu", "Baray Gal"],
        "Mentions": [125, 98, 44, 39, 20]
    })

    st.bar_chart(sample_data.set_index("Party"))

    st.markdown("#### 🧠 Sentiment & Comment Summary")
    st.info("Comment sentiment and summaries will appear here after analysis is added.")

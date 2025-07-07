
import streamlit as st
import requests
import pandas as pd
from urllib.parse import urlparse, parse_qs

access_token = "EAAQuTsUxpHYBPEu0IRwY8I8zyTZCltrEibmGWqpddYoGMl0sRpJrtn6EHtdTsxo9MStz5cfDPGcE5DZAoP56HkAcQgbqL36wWnpZC58VYmeCBcNNqoot5OCUX2TaprWTZBod6bPyTf3O2giU1zK3bLkburiIgkZCYwE9VGcA2JSLviZCDTWIbIrGUYfcdoePxxEE5y9Fryb6D4CXZAmcN4Nl7DrZCk4PZCuHZCIlZCfTaZCAjNpWzEZAFP1GAXJaIzJmhuZAWlclCktB2hyZAtUTQZDZD"

def resolve_final_facebook_url(url):
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        final_url = response.url
        return final_url
    except Exception as e:
        return None

def extract_post_id(url):
    import re
    url = resolve_final_facebook_url(url) or url

    patterns = [
        r"posts/(\d+)",
        r"photo\?fbid=(\d+)",
        r"story_fbid=(\d+)",
        r"videos/(\d+)",
        r"/permalink/(\d+)",
        r"/(\d{5,})/?$"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def fetch_comments(post_id):
    comments = []
    url = f"https://graph.facebook.com/v17.0/{post_id}/comments"
    params = {
        "access_token": access_token,
        "limit": 500,
        "summary": "true"
    }

    while url:
        response = requests.get(url, params=params)
        data = response.json()
        if "data" in data:
            comments.extend(data["data"])
        else:
            break
        if "paging" in data and "next" in data["paging"]:
            url = data["paging"]["next"]
            params = {}
        else:
            break
    return comments

def facebook_post_survey():
    st.title("📊 Facebook Post Comment Survey (Supports all links)")
    post_url = st.text_input("🔗 Facebook post/share/photo link")

    if post_url:
        with st.spinner("🔍 Resolving Facebook link..."):
            post_id = extract_post_id(post_url)

        if post_id:
            st.success(f"✅ Post ID Detected: {post_id}")
            if st.button("📥 Fetch ALL Comments & Convert to CSV"):
                with st.spinner("📡 Fetching comments (up to 100K+)..."):
                    comments = fetch_comments(post_id)
                if comments:
                    df = pd.DataFrame(comments)
                    csv_path = "/mnt/data/comments_output.csv"
                    df.to_csv(csv_path, index=False)
                    st.success(f"✅ {len(comments)} comments saved to CSV.")
                    st.download_button("Download CSV", data=df.to_csv(index=False), file_name="comments.csv", mime="text/csv")
                    st.session_state.comments_df = df
                else:
                    st.warning("⚠️ No comments found or access denied.")
        else:
            st.error("❌ Unable to extract valid Post ID from the link.")

    if st.session_state.get("comments_df") is not None:
        df = st.session_state.comments_df
        st.markdown("### 🧠 Simulated Analysis")
        st.dataframe(df[["from", "message"]].head(10))

facebook_post_survey()

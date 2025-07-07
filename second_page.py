
import streamlit as st
import requests
import pandas as pd
from urllib.parse import urlparse, parse_qs

access_token = "EAAQuTsUxpHYBPMdwr12q9ASrFkrvHW35rkM9QPGIzHsGT6HB5b0nRMHhygop3m4A71E28JZBA6EBawt9qmDtZBeiOUarhvRMiztVfIn64EonZCDArQT7ulNw6xkt7L3xLOdGMliuTa8onSZAxMnsFNXVrUrYt6EoMSAgooHrtVDgyK7QRIjL0GErZCEvJkVmHsar1Kw57MlmdBs4dJEVTLzjOACQRZBHAxRZCoZBLf9z9QZC93ZCdUSiD8wuJEsZC3WCAfAnskLqUenlvZB9"

def resolve_final_facebook_url(url):
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        return response.url
    except Exception:
        return url

def extract_post_id(url):
    import re
    url = resolve_final_facebook_url(url)
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

        if "error" in data:
            return {"error": data["error"].get("message", "Unknown error")}

        if "data" in data:
            comments.extend(data["data"])
        else:
            break

        if "paging" in data and "next" in data["paging"]:
            url = data["paging"]["next"]
            params = {}
        else:
            break
    return {"comments": comments}

def facebook_post_survey():
    st.title("📊 Facebook Page Post Comment Survey (Live Mode)")

    post_url = st.text_input("🔗 Facebook Page post/share/photo link")

    if post_url:
        with st.spinner("🔍 Resolving link and detecting Post ID..."):
            post_id = extract_post_id(post_url)

        if post_id:
            st.success(f"✅ Post ID Detected: {post_id}")

            if st.button("📥 Fetch ALL Comments & Convert to CSV"):
                with st.spinner("📡 Fetching comments..."):
                    result = fetch_comments(post_id)

                if "error" in result:
                    st.error(f"❌ Facebook API Error: {result['error']}")
                elif result.get("comments"):
                    comments = result["comments"]
                    df = pd.DataFrame(comments)
                    csv_path = "/mnt/data/comments_output.csv"
                    df.to_csv(csv_path, index=False)
                    st.success(f"✅ {len(comments)} comments saved to CSV.")
                    st.download_button("Download CSV", data=df.to_csv(index=False), file_name="comments.csv", mime="text/csv")
                    st.session_state.comments_df = df
                else:
                    st.warning("⚠️ No comments found.")
        else:
            st.error("❌ Could not extract valid Post ID from the link.")

    if st.session_state.get("comments_df") is not None:
        df = st.session_state.comments_df
        st.markdown("### 🧠 Simulated Analysis Preview")
        st.dataframe(df[["from", "message"]].head(10))

facebook_post_survey()

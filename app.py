
import streamlit as st
from datetime import datetime
import pandas as pd

from utils.fb_utils import extract_post_id, fetch_comments

from utils.ai_utils import get_sentiment, detect_party
from PIL import Image

# ----------------- Language Packs -----------------
LANG = {
    "English": {
        "login": "Login",
        "username": "Username",
        "password": "Password",
        "login_btn": "Log In",
        "welcome": "Welcome,",
        "date": "Date",
        "analyze": "Analyze Facebook Post",
        "post_link": "Paste Facebook Post URL",
        "fetch": "Fetch Comments",
        "dashboard": "Election Dashboard",
        "logout": "Logout"
    },
    "کوردی": {
        "login": "چوونەژوورەوە",
        "username": "ناوی بەکارهێنەر",
        "password": "وشەی نهێنی",
        "login_btn": "چوونەژوورەوە",
        "welcome": "بەخێربێیت،",
        "date": "ڕێکەوت",
        "analyze": "لیلای پەیامی فەیسبووک",
        "post_link": "بەستەری پەیام بنووسە",
        "fetch": "وەرگرتنی لێدوانەکان",
        "dashboard": "داشبۆردی هەڵبژاردن",
        "logout": "چوونەدەرەوە"
    },
    "العربية": {
        "login": "تسجيل الدخول",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "login_btn": "دخول",
        "welcome": "مرحباً،",
        "date": "التاريخ",
        "analyze": "تحليل منشور فيسبوك",
        "post_link": "الصق رابط المنشور",
        "fetch": "جلب التعليقات",
        "dashboard": "لوحة الانتخابات",
        "logout": "خروج"
    }
}

# ----------------- Session -----------------
if "logged" not in st.session_state:
    st.session_state.logged = False
if "lang" not in st.session_state:
    st.session_state.lang = "English"

# ----------------- Language Selector -----------------
st.session_state.lang = st.selectbox("🌐", list(LANG.keys()), index=list(LANG).index(st.session_state.lang))
L = LANG[st.session_state.lang]

# ----------------- Login Page -----------------
def login_page():
    st.title(L["login"])
    user = st.text_input(L["username"])
    pw = st.text_input(L["password"], type="password")
    if st.button(L["login_btn"]):
        if user == st.secrets.get("USERNAME", "shvan") and pw == st.secrets.get("PASSWORD", "shvan1234"):
            st.session_state.logged = True
            st.experimental_rerun()
        else:
            st.error("❌ Wrong credentials")

if not st.session_state.logged:
    login_page()
st.stop()

# ----------------- Header -----------------
try:
    st.image("puk_logo.png", width=100)
except Exception as e:
    st.warning(f"Logo error: {e}")

st.markdown(f"### {L['welcome']} **Shvan Qaraman**")
st.markdown(f"**{L['date']}:** {datetime.now().strftime('%Y-%m-%d')}")

if st.button(L["logout"]):
    st.session_state.logged = False
    st.experimental_rerun()

# ----------------- Facebook Post Analyzer -----------------
st.header(L["analyze"])
link = st.text_input(L["post_link"])
if st.button(L["fetch"]):
    if not link:
        st.warning("Please enter a valid Facebook post link.")
    else:
        post_id = extract_post_id(link)
        token = st.secrets["FB_ACCESS_TOKEN"]
        st.info("Fetching comments from Facebook...")
        raw_comments = fetch_comments(post_id, token)
        if not raw_comments:
            st.error("No comments found or token expired.")
    st.stop()

# Simple city match in comment text
city_keywords = ["Erbil", "Sulaimani", "Duhok", "Kirkuk"]
cities = []
for comment in raw_comments:
    city_found = next((c for c in city_keywords if c.lower() in comment.lower()), "Unknown")
    cities.append(city_found)

    df = pd.DataFrame({"Comment": raw_comments, "City": cities})
    df["Sentiment"] = df["Comment"].apply(get_sentiment)
    df["Party"] = df["Comment"].apply(detect_party)
st.success(f"Fetched {len(df)} comments.")
st.dataframe(df)

st.download_button("Download CSV", data=df.to_csv(index=False), file_name="comments.csv")

st.subheader("City Distribution")
city_chart = df["City"].value_counts().reset_index()
city_chart.columns = ["City", "Comments"]
st.bar_chart(city_chart.set_index("City"))
        st.stop()

    # --- Simulated data. Replace with real Facebook fetch utils.fb_fetch.fetch_all_comments
    comments = ["Vote PUK", "Need change in Erbil", "KDP is strong", "PUK forever"]
    cities = ["Erbil", "Sulaimani", "Erbil", "Kirkuk"]

    df = pd.DataFrame({"Comment": comments, "City": cities})
    st.success(f"Fetched {len(df)} comments.")
    st.dataframe(df)

    st.subheader("City Distribution")
    city_chart = df["City"].value_counts().reset_index()
    city_chart.columns = ["City", "Comments"]
    st.bar_chart(city_chart.set_index("City"))

    st.subheader("Sentiment Distribution")
    sentiment_counts = df["Sentiment"].value_counts()
    st.bar_chart(sentiment_counts)

    st.subheader("Party Mentions")
    party_counts = df["Party"].value_counts()
    st.bar_chart(party_counts)

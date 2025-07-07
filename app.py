
import streamlit as st
import dashboard  # new dashboard file

# Login system
users = {"shvan": "shvan"}

st.set_page_config(page_title="PUK AI Dashboard", layout="wide")
st.image("puk_logo.png", width=150)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("PUK Election AI Dashboard Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.success("✅ Logged in successfully!")
        else:
            st.error("❌ Invalid credentials")
else:
    dashboard.load_dashboard()  # load main dashboard


import streamlit as st
import second_page

st.image("puk_logo.png", width=150)

users = {"shvan": "shvan"}

st.title("PUK Election AI Dashboard (Login)")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.success("✅ Logged in successfully!")
            st.experimental_rerun()
        else:
            st.error("❌ Invalid credentials")
else:
    second_page.facebook_post_survey()

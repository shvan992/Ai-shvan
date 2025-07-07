
import streamlit as st

# Display PUK logo
st.image("puk_logo.png", width=150)

# Login system
users = {"shvan": "shvan"}

st.title("PUK Election AI Dashboard (Minimal Test)")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username in users and users[username] == password:
        st.success("✅ Logged in successfully!")
        st.markdown("Welcome to the minimal version of the dashboard.")
    else:
        st.error("❌ Invalid credentials")

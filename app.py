
import streamlit as st

# Language selector
language = st.selectbox("Select Language", ["English", "Kurdish", "Arabic"])

# Simulated login
username = st.text_input("Username")
password = st.text_input("Password", type="password")
if st.button("Login") and username == "shvan" and password == "shvan1234":
    st.success("Logged in successfully!")
    st.markdown("# Facebook Post & Comment Analyzer")
    st.write("Upload or paste Facebook post link below:")
    st.text_input("Facebook Link")
    st.button("Fetch Comments and Analyze")
    st.write("Charts and data will appear here...")
else:
    st.warning("Please login to access the dashboard.")

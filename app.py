
import streamlit as st

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Fake login system (replace with real authentication logic)
def login():
    st.title("PUK AI Dashboard Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin":  # Replace with real check
            st.session_state.logged_in = True
        else:
            st.error("Invalid credentials")

# Dashboard page
def show_dashboard():
    st.set_page_config(page_title="PUK AI Dashboard", layout="wide")
    st.markdown("<h1>PUK Election AI Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("Prepared by Shvan Qaraman", unsafe_allow_html=True)
    st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"])
    st.button("Analyze CSV")

# Language selector
lang = st.selectbox("Language", ["English", "Kurdish", "Arabic"])

# Main logic
if st.session_state.logged_in:
    show_dashboard()
else:
    login()

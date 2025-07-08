
import streamlit as st

st.set_page_config(page_title="PUK AI Dashboard", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def show_login():
    st.image("logo.png", width=120)
    st.title("PUK AI Dashboard")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "shvan" and password == "shvan":
            st.session_state.logged_in = True
        else:
            st.warning("Invalid credentials")

def show_dashboard():
    st.success("Welcome to the Dashboard!")
    st.write("This will contain charts, analyzers, uploaders, etc.")

if not st.session_state.logged_in:
    show_login()
else:
    show_dashboard()

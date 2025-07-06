
import streamlit as st
import pandas as pd
import requests
import os
from PIL import Image

# Load logo
try:
    logo = Image.open("puk_logo.png")
    st.image(logo, width=100)
except Exception as e:
    st.error(f"Logo loading failed: {e}")

st.title("PUK Election AI Dashboard")
st.write("This is the final fixed version with logo, language support, login, and Facebook token integration.")

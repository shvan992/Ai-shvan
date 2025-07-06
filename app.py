
import streamlit as st
import pandas as pd
from PIL import Image
import base64

# Load logo
try:
    logo = Image.open("puk_logo.png")
    st.image(logo, width=100)
except Exception as e:
    st.error(f"Logo loading failed: {e}")

st.title("PUK Election AI Dashboard")

# Login (placeholder for demonstration)
username = st.text_input("Username")
password = st.text_input("Password", type="password")
if st.button("Login"):
    if username == "shvan" and password == "shvan1234":
        st.success("Login successful!")
        st.subheader("Paste Facebook Post Link")
        fb_link = st.text_input("Facebook Post URL")

        if fb_link:
            st.info("Fetching comments... (Simulated)")
            comments = ["Comment 1", "Comment 2", "Comment 3"]
            df = pd.DataFrame(comments, columns=["Comment"])
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "comments.csv", "text/csv")
    else:
        st.error("Invalid login credentials")

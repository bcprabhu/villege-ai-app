import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
from PIL import Image  # This must stay at the top

# 1. ALWAYS FIRST: Set the page config
st.set_page_config(page_title="Village AI Super App", page_icon="🚜")

# 2. Connect to Gemini
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("API Key missing!")

# 3. NOW add the Logo and Sidebar
try:
    logo_img = Image.open("logo.jpg")
    st.sidebar.image(logo_img, use_container_width=True)
except Exception as e:
    # This will show a small note in the sidebar if the image file is missing
    st.sidebar.info("Logo image not found. Please ensure 'logo.jpg' is uploaded to GitHub.")

st.sidebar.title("Settings")
# ... (rest of your code for language_choice and location follows here)

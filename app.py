import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
from PIL import Image

# --- 1. SET PAGE CONFIG (MUST BE FIRST) ---
st.set_page_config(page_title="Village AI Super App", page_icon="🚜", layout="wide")

# --- 2. LOGO LOADING (SAFE MODE) ---
try:
    # This tries to load the image but won't crash the app if it fails
    logo = Image.open("logo.jpg")
    st.sidebar.image(logo, use_container_width=True)
except Exception:
    st.sidebar.warning("Logo file 'logo.jpg' not found on GitHub.")

# --- 3. SETTINGS & CONNECTIONS ---
st.sidebar.title("Settings")
language_choice = st.sidebar.selectbox("Language / भाषा", ("Hindi", "English", "Marathi", "Telugu", "Tamil", "Kannada", "Bengali"))
location = st.sidebar.text_input("Village/District:", value="Nagpur")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("API Key missing in Secrets!")

# --- 4. MAIN APP CONTENT (THE RIGHT SIDE) ---
st.title("🚜 Village AI Super App")

tab1, tab2, tab3 = st.tabs(["💬 Ask AI", "📸 Plant Doctor", "📊 Mandi & Weather"])

with tab1:
    user_q = st.text_input("Ask a question / सवाल पूछें:")
    if st.button("Get Answer"):
        if user_q:
            response = model.generate_content(f"Answer simply in {language_choice}: {user_q}")
            st.success(response.text)
# ... rest of your code ...

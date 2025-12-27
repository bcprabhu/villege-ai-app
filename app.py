import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
from PIL import Image

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="Village AI Super App", page_icon="🚜", layout="wide")

# --- 2. LOGO LOADING ---
try:
    logo = Image.open("logo.jpg")
    st.sidebar.image(logo, use_container_width=True)
except Exception:
    st.sidebar.info("Upload logo.jpg to see the farmer image.")

# --- 3. SETTINGS & CREATOR INFO ---
st.sidebar.title("Settings / ಸಂಯೋಜನೆಗಳು")

language_choice = st.sidebar.selectbox(
    "Choose Language / ಭಾಷೆಯನ್ನು ಆರಿಸಿ",
    ("Hindi", "English", "Marathi", "Telugu", "Tamil", "Kannada", "Bengali"),
    index=5 # Defaults to Kannada
)

location = st.sidebar.text_input("Village/District (ಹಳ್ಳಿ/ಜಿಲ್ಲೆ):", value="Bengaluru")

# --- CREATOR SIGNATURE ---
st.sidebar.markdown("---")
st.sidebar.write("👨‍🏫 **Created By:**")
st.sidebar.write("**B.C. Prabhakar**")
st.sidebar.caption("Freelance Oil and Gas Engineering Consultant")

# --- 4. CONNECTIONS ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("API Key missing!")

def speak(text, lang_code):
    try:
        lang_map = {"Hindi": "hi", "English": "en", "Marathi": "mr", "Telugu": "te", "Tamil": "ta", "Kannada": "kn", "Bengali": "bn"}
        tts = gTTS(text=text, lang=lang_map[language_choice])
        tts.save("voice.mp3")
        with open("voice.mp3", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except:
        pass

# --- 5. MAIN CONTENT ---
st.title("🚜 Village AI Super App")
st.subheader("Your Digital Farming Expert / ನಿಮ್ಮ ಕೃಷಿ ತಜ್ಞ")

with st.expander("📖 Instructions / ಸೂಚನೆಗಳು"):
    st.write("1. Ask questions. 2. Take plant photos. 3. Check Mandi prices.")

tab1, tab2, tab3 = st.tabs(["💬 Ask AI", "📸 Plant Doctor", "📊 Mandi & Weather"])

with tab1:
    user_q = st.text_input("Ask a question / ಪ್ರಶ್ನೆ ಕೇಳಿ:")
    if st.button("Get Answer"):
        if user_q:
            with st.spinner("Thinking..."):
                response = model.generate_content(f"Answer simply in {language_choice}: {user_q}")
                st.success(response.text)
                speak(response.text, language_choice)

with tab2:
    st.write("Upload or take a photo of a crop problem.")
    img_file = st.camera_input("Capture Crop Image")
    if img_file:
        img = Image.open(img_file)
        if st.button("Analyze Plant"):
            with st.spinner("Analyzing..."):
                response = model.generate_content([f"Identify the plant problem in this image and suggest a solution in {language_choice}.", img])
                st.success(response.text)
                speak(response.text, language_choice)

with tab3:
    st.header(f"Live Updates: {location}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Mandi Prices"):
            response = model.generate_content(f"Give latest crop prices for {location} in {language_choice}.")
            st.info(response.text)
    with col2:
        if st.button("Weather Forecast"):
            response = model.generate_content(f"Give 2-day weather for {location} in {language_choice}.")
            st.warning(response.text)

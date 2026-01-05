import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
from PIL import Image
import urllib.parse

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="Village AI Super App", page_icon="🚜", layout="wide")

# --- 2. LOGO LOADING ---
try:
    logo = Image.open("logo.jpg")
    st.sidebar.image(logo, use_container_width=True)
except Exception:
    st.sidebar.info("Upload logo.jpg to see the farmer image.")

# --- 3. SIDEBAR SETTINGS ---
st.sidebar.title("Settings / ಸಂಯೋಜನೆಗಳು")
language_choice = st.sidebar.selectbox(
    "Choose Language / ಭಾಷೆಯನ್ನು ಆರಿಸಿ",
    ("Hindi", "English", "Marathi", "Telugu", "Tamil", "Kannada", "Bengali"),
    index=5
)
location = st.sidebar.text_input("Village/District (ಹಳ್ಳಿ/ಜಿಲ್ಲೆ):", value="Bengaluru")

st.sidebar.markdown("---")
st.sidebar.write("👨‍🏫 **Created By:**")
st.sidebar.write("**B.C. Prabhakar**")

# --- 4. CONNECTIONS & LOGIC ---
# This is the fix for the 404 error
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # We use 1.5-flash because it is the world leader for audio/voice apps
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API Key missing in Secrets!")

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

tab1, tab2, tab3 = st.tabs(["💬 Ask AI", "📸 Plant Doctor", "📊 Mandi & Weather"])

with tab1:
    st.write("### 🎤 Speak Your Question / ಮಾತನಾಡಿ")
    
    # Official stable audio input
    audio_file = st.audio_input("Tap the mic and speak (3–5 seconds)")

    if audio_file:
        with st.spinner("Analyzing your voice..."):
            try:
                audio_bytes = audio_file.getvalue()
                # Package audio for Gemini 1.5
                response = model.generate_content([
                    f"You are a helpful farming expert. Answer the user's question in {language_choice}.",
                    {"mime_type": "audio/wav", "data": audio_bytes}
                ])
                st.success(response.text)
                speak(response.text, language_choice)
            except Exception as e:
                st.error("Voice processing error. Please use the buttons below.")

    st.markdown("---")
    st.write("### Quick Help / ತ್ವರಿತ ಸಹಾಯ")
    
    col1, col2 = st.columns(2)
    query = ""

    with col1:
        if st.button("🌾 Rice/Paddy Tips"):
            query = "Give me 5 tips for high yield in Paddy farming."
        if st.button("🍅 Tomato Diseases"):
            query = "Common Tomato diseases and cures."
    with col2:
        if st.button("💧 Save Water"):
            query = "Best irrigation methods to save water."
        if st.button("💰 Govt Schemes"):
            query = "Top 3 government schemes for Indian farmers."

    st.markdown("---")
    user_q = st.text_input("Or type here (ಅಥವಾ ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ):", value=query)
    
    if st.button("Get Answer", key="q_btn"):
        if user_q:
            with st.spinner("Thinking..."):
                response = model.generate_content(f"Answer simply in {language_choice}: {user_q}")
                st.success(response.text)
                speak(response.text, language_choice)

with tab2:
    st.write("### 📸 Plant Doctor")
    img_file = st.camera_input("Capture Crop Image")
    if img_file:
        img = Image.open(img_file)
        if st.button("Analyze Plant"):
            with st.spinner("Analyzing..."):
                response = model.generate_content([f"Identify the plant problem in this image and suggest a solution in {language_choice}.", img])
                st.success(response.text)
                speak(response.text, language_choice)

with tab3:
    st.write("### 📊 Mandi & Weather")
    st.header(f"Updates for: {location}")
    if st.button("Get Live Updates"):
        with st.spinner("Fetching..."):
            response = model.generate_content(f"Give crop prices and 2-day weather for {location} in {language_choice}.")
            st.info(response.text)

import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
from PIL import Image
import os
import re

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="Village AI Super App", page_icon="🚜", layout="wide")

# --- 2. SIDEBAR & STOP BUTTON ---
st.sidebar.title("Settings / ಸಂಯೋಜನೆಗಳು")
language_choice = st.sidebar.selectbox(
    "Choose Language / ಭಾಷೆಯನ್ನು ಆರಿಸಿ",
    ("Hindi", "English", "Marathi", "Telugu", "Tamil", "Kannada", "Bengali"),
    index=5
)
location = st.sidebar.text_input("Village/District:", value="Bengaluru")

st.sidebar.markdown("---")
# THE STOP BUTTON: Clicking this will stop the voice and reset the page
if st.sidebar.button("🛑 STOP VOICE (ಧ್ವನಿ ನಿಲ್ಲಿಸಿ)"):
    st.rerun()

# --- 3. PERSONALITY & CLEANING ---
# We tell the AI to be VERY short and use NO symbols
SYSTEM_PROMPT = f"""
You are a friendly village farming expert. 
1. Speak in {language_choice} only.
2. IMPORTANT: Do NOT use any symbols like * or # or stars. 
3. Be extremely brief (maximum 2-3 sentences).
4. Do NOT repeat the user's question. 
"""

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction=SYSTEM_PROMPT
    )
else:
    st.error("API Key missing!")

def speak(text):
    try:
        # CLEANING: This removes * symbols so the AI doesn't say "Nakshatra Chinne"
        clean_text = re.sub(r'[*#]', '', text)
        
        lang_map = {"Hindi": "hi", "English": "en", "Marathi": "mr", "Telugu": "te", "Tamil": "ta", "Kannada": "kn", "Bengali": "bn"}
        tts = gTTS(text=clean_text, lang=lang_map[language_choice])
        tts.save("temp_voice.mp3")
        with open("temp_voice.mp3", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        
        # Displaying the audio player so you can also pause it manually
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except:
        pass

# --- 4. MAIN CONTENT ---
st.title("🚜 Village AI Super App")

tab1, tab2, tab3 = st.tabs(["💬 Ask AI", "📸 Plant Doctor", "📊 Mandi & Weather"])

with tab1:
    st.write("### 🎤 Ask Your Question")
    audio_file = st.audio_input("Tap the mic and speak")

    if audio_file:
        with st.spinner("Listening..."):
            try:
                audio_bytes = audio_file.getvalue()
                response = model.generate_content([
                    {"mime_type": "audio/wav", "data": audio_bytes},
                    "Answer briefly in 2 sentences."
                ])
                st.success(response.text)
                speak(response.text)
            except:
                st.error("Glich! Try again.")

    st.markdown("---")
    user_q = st.text_input("Or type here:")
    if st.button("Get Answer") and user_q:
        response = model.generate_content(user_q)
        st.success(response.text)
        speak(response.text)

with tab2:
    st.write("### 📸 Plant Doctor")
    img_file = st.camera_input("Take photo")
    if img_file:
        img = Image.open(img_file)
        if st.button("Check My Crop"):
            response = model.generate_content(["Identify this problem in 1 sentence.", img])
            st.info(response.text)
            speak(response.text)

with tab3:
    st.write("### 📊 Mandi Updates")
    if st.button("Check Prices"):
        response = model.generate_content(f"Give crop prices for {location} in 2 sentences.")
        st.write(response.text)
        speak(response.text)

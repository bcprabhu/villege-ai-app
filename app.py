import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
from PIL import Image
import os
import re

# --- 1. SET PAGE CONFIG (MUST BE FIRST) ---
st.set_page_config(
    page_title="Village AI Super App",
    page_icon="🚜",
    layout="wide"
)

# --- 2. SIDEBAR & CONTROLS ---
st.sidebar.title("Settings / ಸಂಯೋಜನೆಗಳು")
language_choice = st.sidebar.selectbox(
    "Choose Language / ಭಾಷೆಯನ್ನು ಆರಿಸಿ",
    ("Hindi", "English", "Marathi", "Telugu", "Tamil", "Kannada", "Bengali"),
    index=5
)
location = st.sidebar.text_input("Village/District:", value="Bengaluru")

st.sidebar.markdown("---")
# THE STOP BUTTON
if st.sidebar.button("🛑 STOP VOICE (ಧ್ವನಿ ನಿಲ್ಲಿಸಿ)", use_container_width=True):
    st.rerun()

st.sidebar.write("👨‍🏫 **Created By: B.C. Prabhakar**")

# --- 3. PERSONALITY & VOICE LOGIC ---
SYSTEM_PROMPT = f"""
You are a friendly, wise village farming expert. 
1. Speak in {language_choice} only.
2. IMPORTANT: Do NOT use any symbols like * or # or stars in your text.
3. Keep answers very brief (max 2-3 sentences).
4. No 'Nakshatra Chinne'. Speak like a normal human.
"""

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction=SYSTEM_PROMPT
    )
else:
    st.error("API Key missing in Streamlit Secrets!")

def speak(text):
    try:
        # CLEANING: Removes * and # so the AI doesn't say "Nakshatra Chinne"
        clean_text = re.sub(r'[*#]', '', text)
        lang_map = {"Hindi": "hi", "English": "en", "Marathi": "mr", "Telugu": "te", "Tamil": "ta", "Kannada": "kn", "Bengali": "bn"}
        tts = gTTS(text=clean_text, lang=lang_map[language_choice])
        tts.save("temp_voice.mp3")
        with open("temp_voice.mp3", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except:
        pass

# --- 4. MAIN INTERFACE ---
st.title("🚜 Village AI Super App")

tab1, tab2, tab3 = st.tabs(["💬 Ask AI", "📸 Plant Doctor", "📊 Mandi & Weather"])

with tab1:
    st.write("### 🎤 Talk to your Expert")
    audio_file = st.audio_input("Tap the mic and speak")

    if audio_file:
        with st.spinner("Listening..."):
            try:
                audio_bytes = audio_file.getvalue()
                response = model.generate_content([
                    {"mime_type": "audio/wav", "data": audio_bytes},
                    "Answer briefly."
                ])
                st.chat_message("assistant").write(response.text)
                speak(response.text)
            except:
                st.error("Connection error. Try again.")

    st.markdown("---")
    st.write("### 💡 Quick Help / ತ್ವರಿತ ಸಹಾಯ")
    
    col1, col2 = st.columns(2)
    selected_query = ""

    with col1:
        if st.button("🌾 Rice/Paddy Tips", use_container_width=True):
            selected_query = "Give me 3 tips for high yield in Paddy."
        if st.button("🍅 Tomato Diseases", use_container_width=True):
            selected_query = "Common Tomato diseases and cures."
        if st.button("🐛 Pest Control", use_container_width=True):
            selected_query = "Organic ways to control pests."

    with col2:
        if st.button("💧 Save Water", use_container_width=True):
            selected_query = "Best irrigation methods to save water."
        if st.button("🌱 Organic Fertilizer", use_container_width=True):
            selected_query = "How to make organic fertilizer at home?"
        if st.button("💰 Govt Schemes", use_container_width=True):
            selected_query = "Top 2 government schemes for farmers."

    st.markdown("---")
    user_q = st.text_input("Or type here (ಅಥವಾ ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ):", value=selected_query)
    
    if st.button("Get Answer", type="primary") or (selected_query != ""):
        if user_q:
            with st.spinner("Thinking..."):
                response = model.generate_content(user_q)
                st.chat_message("assistant").write(response.text)
                speak(response.text)

with tab2:
    st.write("### 📸 Plant Doctor")
    img_file = st.camera_input("Capture Crop Image")
    if img_file:
        img = Image.open(img_file)
        if st.button("Analyze Plant"):
            with st.spinner("Analyzing..."):
                response = model.generate_content(["Identify the problem and solution in 2 sentences.", img])
                st.success(response.text)
                speak(response.text)

with tab3:
    st.write("### 📊 Mandi & Weather")
    st.header(f"Updates for: {location}")
    if st.button("Get Live Updates"):
        with st.spinner("Fetching..."):
            response = model.generate_content(f"Crop prices and weather for {location} in 2 sentences.")
            st.info(response.text)
            speak(response.text)

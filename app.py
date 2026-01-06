import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
from PIL import Image
import os
import re
import urllib.parse

# --- 1. SET PAGE CONFIG ---
st.set_page_config(
    page_title="Village AI Super App",
    page_icon="🚜",
    layout="wide"
)

# --- 2. SIDEBAR & SETTINGS ---
st.sidebar.title("Settings / ಸಂಯೋಜನೆಗಳು")
language_choice = st.sidebar.selectbox(
    "Choose Language / ಭಾಷೆಯನ್ನು ಆರಿಸಿ",
    ("Hindi", "English", "Marathi", "Telugu", "Tamil", "Kannada", "Bengali"),
    index=5
)
location = st.sidebar.text_input("Village/District:", value="Bengaluru")

st.sidebar.markdown("---")
if st.sidebar.button("🛑 STOP VOICE (ಧ್ವನಿ ನಿಲ್ಲಿಸಿ)", use_container_width=True):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("👨‍🏫 **Created By: B.C. Prabhakar**")

# --- FEEDBACK BUTTON FIX ---
# REPLACE THE NUMBER BELOW WITH YOUR ACTUAL 10-DIGIT NUMBER
# Example: "919845012345"
phone_number = "919449834721" 
message_text = f"Hello Mr. Prabhakar, I am using your Village AI App in {language_choice}. Here is my feedback: "
encoded_msg = urllib.parse.quote(message_text)
# Updated WhatsApp link format to prevent 404 errors
whatsapp_url = f"https://api.whatsapp.com/send?phone={phone_number}&text={encoded_msg}"

st.sidebar.link_button("💬 Send Feedback (ಪ್ರತಿಕ್ರಿಯೆ)", whatsapp_url, use_container_width=True)

# --- 3. PERSONALITY & VOICE CLEANING ---
SYSTEM_PROMPT = f"""
You are a friendly, wise village farming expert. 
1. Speak in {language_choice} only.
2. IMPORTANT: Do NOT use any symbols like * or # or stars. 
3. Be extremely brief (max 2-3 sentences).
4. Speak like a human neighbor, avoid robotic words.
"""

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction=SYSTEM_PROMPT
    )
else:
    st.error("API Key missing in Secrets!")

def speak(text):
    try:
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
    st.write("### 🎤 Talk to Expert (ಮಾತನಾಡಿ)")
    audio_file = st.audio_input("Tap the mic and speak clearly")

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
                st.error("Error hearing voice. Please try typing.")

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
    img_file = st.camera_input("Take photo of crop")
    if img_file:
        img = Image.open(img_file)
        if st.button("Check My Crop"):
            with st.spinner("Analyzing..."):
                response = model.generate_content(["Identify this problem in 2 sentences.", img])
                st.info(response.text)
                speak(response.text)

with tab3:
    st.write("### 📊 Mandi Updates")
    if st.button("Get Live Updates"):
        with st.spinner("Fetching..."):
            response = model.generate_content(f"Crop prices and weather for {location} in 2 sentences.")
            st.success(response.text)
            speak(response.text)

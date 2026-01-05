import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
from PIL import Image
import os

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="Village AI Super App", page_icon="🚜", layout="wide")

# --- 2. LOGO LOADING ---
try:
    if os.path.exists("logo.jpg"):
        logo = Image.open("logo.jpg")
        st.sidebar.image(logo, use_container_width=True)
except:
    pass

# --- 3. SIDEBAR ---
st.sidebar.title("Settings / ಸಂಯೋಜನೆಗಳು")
language_choice = st.sidebar.selectbox(
    "Choose Language / ಭಾಷೆಯನ್ನು ಆರಿಸಿ",
    ("Hindi", "English", "Marathi", "Telugu", "Tamil", "Kannada", "Bengali"),
    index=5
)
location = st.sidebar.text_input("Village/District:", value="Bengaluru")

# --- 4. THE PERSONALITY (System Instruction) ---
# This is what makes it funny and conversational
SYSTEM_PROMPT = f"""
You are a friendly, wise, and slightly funny village farming expert. 
Your tone is conversational, like a neighbor talking over a fence.
RULES:
1. Speak in {language_choice} only.
2. Do NOT repeat the user's question back to them.
3. Be short and direct. No long 'artificial' paragraphs.
4. Use a bit of farming humor or village wisdom.
5. If the user asks something non-farming, joke that you only have 'crop-brains'.
"""

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Applying the personality here
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction=SYSTEM_PROMPT
    )
else:
    st.error("API Key missing!")

def speak(text):
    try:
        lang_map = {"Hindi": "hi", "English": "en", "Marathi": "mr", "Telugu": "te", "Tamil": "ta", "Kannada": "kn", "Bengali": "bn"}
        tts = gTTS(text=text, lang=lang_map[language_choice])
        tts.save("temp_voice.mp3")
        with open("temp_voice.mp3", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        # The 'key' ensures it doesn't play twice
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
        os.remove("temp_voice.mp3")
    except:
        pass

# --- 5. MAIN APP ---
st.title("🚜 Village AI Super App")

tab1, tab2, tab3 = st.tabs(["💬 Ask AI", "📸 Plant Doctor", "📊 Mandi & Weather"])

with tab1:
    st.write("### 🎤 Talk to your Expert")
    audio_file = st.audio_input("Tap the mic and ask anything!")

    if audio_file:
        with st.spinner("Listening..."):
            try:
                audio_bytes = audio_file.getvalue()
                response = model.generate_content([
                    {"mime_type": "audio/wav", "data": audio_bytes},
                    "Answer as the wise village expert."
                ])
                st.chat_message("assistant").write(response.text)
                speak(response.text)
            except Exception as e:
                st.error("Connection glitch. Try again!")

    st.markdown("---")
    user_q = st.text_input("Or type here:")
    if st.button("Get Answer") and user_q:
        response = model.generate_content(user_q)
        st.chat_message("assistant").write(response.text)
        speak(response.text)

# (Tabs 2 & 3 remain the same as previous versions)
with tab2:
    st.write("### 📸 Plant Doctor")
    img_file = st.camera_input("Take photo")
    if img_file:
        img = Image.open(img_file)
        if st.button("Check My Crop"):
            response = model.generate_content(["What's wrong here? Answer as the wise expert.", img])
            st.write(response.text)
            speak(response.text)

with tab3:
    st.write("### 📊 Mandi Updates")
    if st.button("Check Prices"):
        response = model.generate_content(f"Current Mandi rates for major crops in {location}")
        st.info(response.text)

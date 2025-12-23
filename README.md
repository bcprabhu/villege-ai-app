import streamlit as st
from gtts import gTTS
import base64

# --- THE MAGIC VOICE FUNCTION ---
def speak(text, lang='hi'):
    tts = gTTS(text=text, lang=lang)
    tts.save("speech.mp3")
    with open("speech.mp3", "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    # This creates a hidden audio player that plays automatically
    md = f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
    st.markdown(md, unsafe_allow_html=True)

# --- THE APP INTERFACE ---
st.title("📢 Village AI Assistant / ग्रामीण एआई सहायक")

st.write("Click the button below to hear the message in Hindi.")

if st.button('🔊 Listen / सुनें'):
    message = "नमस्ते, मैं आपका एआई सहायक हूं। मैं खेती और स्वास्थ्य में आपकी मदद कर सकता हूं।"
    st.success(message)
    speak(message, lang='hi') # 'hi' is for Hindi

st.info("AI can speak to those who cannot read.")

import streamlit as st
from gtts import gTTS
import base64

# Function to handle the voice
def speak(text, lang='hi'):
    tts = gTTS(text=text, lang=lang)
    tts.save("speech.mp3")
    with open("speech.mp3", "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    md = f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
    st.markdown(md, unsafe_allow_html=True)

# The App Interface
st.title("📢 Village AI Assistant")
st.header("ग्रामीण एआई सहायक")

st.write("Welcome to the AI awareness app for our village.")

if st.button('🔊 Listen to Greeting (सुनें)'):
    message = "नमस्ते, मैं आपका एआई सहायक हूं। मैं आपकी मदद के लिए तैयार हूं।"
    st.success(message)
    speak(message, lang='hi')

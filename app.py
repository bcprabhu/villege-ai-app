import streamlit as st
from gtts import gTTS
import base64

st.title("📢 Village AI Voice Assistant")
st.header("ग्रामीण एआई सहायक")

if st.button('🔊 Listen / सुनें'):
    msg = "नमस्ते, मैं आपका ग्रामीण एआई सहायक हूं।"
    tts = gTTS(text=msg, lang='hi')
    tts.save("s.mp3")
    with open("s.mp3", "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    st.success(msg)

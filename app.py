import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64

# This part connects to your saved Secret Key
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API Key not found in Secrets!")

st.set_page_config(page_title="Village AI Expert", page_icon="🌾")
st.title("🌾 Village AI Smart Expert")
st.header("ग्रामीण एआई स्मार्ट विशेषज्ञ")

def speak(text):
    tts = gTTS(text=text, lang='hi')
    tts.save("voice.mp3")
    with open("voice.mp3", "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

user_q = st.text_input("Ask any question / कोई भी प्रश्न पूछें:", placeholder="जैसे: जैविक खेती कैसे करें?")

if st.button("Get Expert Answer / जवाब पाएं"):
    if user_q:
        try:
            with st.spinner("AI is thinking..."):
                # This line asks the REAL Google Gemini AI for an answer
                response = model.generate_content(f"You are a helpful village assistant. Answer this briefly in simple Hindi: {user_q}")
                answer = response.text
                
                st.success(answer)
                speak(answer)
        except Exception as e:
            st.error("I'm having trouble connecting to my global brain. Please refresh.")
    else:
        st.warning("Please type a question first.")

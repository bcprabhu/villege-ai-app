import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64

# Connect to Gemini
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # USING THE STABLE 'gemini-pro' MODEL
        model = genai.GenerativeModel('gemini-pro')
    else:
        st.error("API Key not found in Secrets!")
except Exception as e:
    st.error(f"Setup Error: {e}")

st.title("🌾 Village AI Smart Expert")
st.header("ग्रामीण एआई स्मार्ट विशेषज्ञ")

def speak(text):
    tts = gTTS(text=text, lang='hi')
    tts.save("voice.mp3")
    with open("voice.mp3", "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

user_q = st.text_input("Ask about farming or health / खेती या स्वास्थ्य के बारे में पूछें:")

if st.button("Get Expert Answer"):
    if user_q:
        with st.spinner("AI is thinking..."):
            try:
                # Actual AI Call
                response = model.generate_content(f"Answer simply in Hindi: {user_q}")
                answer = response.text
                st.success(answer)
                speak(answer)
            except Exception as e:
                st.error(f"Actual Error: {e}")
    else:
        st.warning("Please type a question.")

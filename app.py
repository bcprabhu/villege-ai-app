import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64

# Connect to the Newest Gemini Brain
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # We are using 2.5-flash because your list showed it is available
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("API Key missing in Secrets!")

st.set_page_config(page_title="Village AI Expert", page_icon="🌾")
st.title("🌾 Village AI Smart Expert")
st.header("ग्रामीण एआई स्मार्ट विशेषज्ञ")

def speak(text):
    try:
        tts = gTTS(text=text, lang='hi')
        tts.save("voice.mp3")
        with open("voice.mp3", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except Exception as e:
        st.warning("Audio play error.")

user_q = st.text_input("Ask a question / प्रश्न पूछें:", placeholder="जैसे: मिट्टी की जांच कैसे करें?")

if st.button("Get Answer / जवाब प्राप्त करें"):
    if user_q:
        with st.spinner("AI is thinking (Gemini 2.5)..."):
            try:
                # Asking the new model
                response = model.generate_content(f"Answer simply in Hindi: {user_q}")
                answer = response.text
                st.success(answer)
                speak(answer)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please type a question first.")

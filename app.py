import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64

# Configure the API Key
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Key not found in Streamlit Secrets!")

st.title("🌾 Village AI Assistant")
st.header("ग्रामीण एआई सहायक")

def speak(text):
    try:
        tts = gTTS(text=text, lang='hi')
        tts.save("voice.mp3")
        with open("voice.mp3", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except:
        pass

user_q = st.text_input("Ask a question / सवाल पूछें:")

if st.button("Get Answer"):
    if user_q:
        with st.spinner("Thinking..."):
            try:
                # This automatically finds the best available model for your key
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"Answer in simple Hindi: {user_q}")
                
                st.success(response.text)
                speak(response.text)
            except Exception as e:
                # If flash fails, try the older Pro version automatically
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(f"Answer in simple Hindi: {user_q}")
                    st.success(response.text)
                    speak(response.text)
                except Exception as e2:
                    st.error(f"Connection Error. Please check your Google AI Studio project status. Error: {e2}")
    else:
        st.warning("Please enter a question.")

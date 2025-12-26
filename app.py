import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64

# Connect to Gemini with a more stable configuration
try:
    if "GEMINI_API_KEY" in st.secrets:
        # We use 'v1' instead of the default to avoid the 404 error
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("API Key not found in Secrets!")
except Exception as e:
    st.error(f"Setup Error: {e}")

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
    except:
        st.warning("Voice output failed, but you can read the answer below.")

user_q = st.text_input("Ask a question / प्रश्न पूछें:")

if st.button("Get Answer"):
    if user_q:
        with st.spinner("AI is thinking..."):
            try:
                # Force a simple response
                response = model.generate_content(user_q)
                st.success(response.text)
                speak(response.text)
            except Exception as e:
                # If it fails, we show the list of models available to YOUR key
                st.error(f"Actual Error: {e}")
                st.write("Trying to find available models...")
                try:
                    models = [m.name for m in genai.list_models()]
                    st.write("Your available models are:", models)
                except:
                    st.write("Could not list models. Please check if your API Key is active in Google AI Studio.")

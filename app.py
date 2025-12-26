import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64

# Connect to Gemini 2.5
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("API Key missing!")

st.set_page_config(page_title="Multi-Language Village AI", page_icon="🌾")

# --- SIDEBAR FOR SETTINGS ---
st.sidebar.title("Settings / सेटिंग्स")
language_choice = st.sidebar.selectbox(
    "Choose Language / भाषा चुनें",
    ("Hindi", "English", "Marathi", "Telugu", "Tamil", "Kannada", "Bengali")
)

# Mapping languages to gTTS codes
lang_codes = {
    "Hindi": "hi", "English": "en", "Marathi": "mr", 
    "Telugu": "te", "Tamil": "ta", "Kannada": "kn", "Bengali": "bn"
}

st.title("🌾 Village AI Smart Expert")
st.write(f"Currently helping you in: **{language_choice}**")

def speak(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code)
        tts.save("voice.mp3")
        with open("voice.mp3", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except:
        pass

user_q = st.text_input("Ask your question here / अपना प्रश्न यहाँ लिखें:")

if st.button("Get Answer"):
    if user_q:
        with st.spinner(f"Thinking in {language_choice}..."):
            try:
                # We tell the AI which language to use based on the selection
                prompt = f"You are a village expert. Answer this question simply in {language_choice}: {user_q}"
                response = model.generate_content(prompt)
                
                answer = response.text
                st.success(answer)
                
                # Speak in the selected language
                speak(answer, lang_codes[language_choice])
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please type a question.")

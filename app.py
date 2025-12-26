import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
from PIL import Image

# Connect to Gemini 2.5
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("API Key missing!")

st.set_page_config(page_title="Village AI Expert", page_icon="🌾")

# --- SIDEBAR ---
st.sidebar.title("Settings")
language_choice = st.sidebar.selectbox(
    "Choose Language",
    ("Hindi", "English", "Marathi", "Telugu", "Tamil", "Kannada", "Bengali")
)

lang_codes = {"Hindi": "hi", "English": "en", "Marathi": "mr", "Telugu": "te", "Tamil": "ta", "Kannada": "kn", "Bengali": "bn"}

st.title("🌾 Village AI Smart Expert")

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

# --- TABBED INTERFACE ---
tab1, tab2 = st.tabs(["💬 Ask a Question", "📸 Plant Doctor (Camera)"])

with tab1:
    user_q = st.text_input("Type your question:")
    if st.button("Get Answer"):
        if user_q:
            with st.spinner("Thinking..."):
                response = model.generate_content(f"Answer simply in {language_choice}: {user_q}")
                st.success(response.text)
                speak(response.text, lang_codes[language_choice])

with tab2:
    st.write("Take a photo of a sick plant or pest to get help.")
    img_file = st.camera_input("Take a Photo")
    
    if img_file:
        img = Image.open(img_file)
        st.image(img, caption="Uploaded Image", use_container_width=True)
        
        if st.button("Identify Problem"):
            with st.spinner("Analyzing Image..."):
                # Sending both image and text to Gemini
                response = model.generate_content([f"Identify the plant problem in this image and suggest a solution in {language_choice}.", img])
                st.success(response.text)
                speak(response.text, lang_codes[language_choice])

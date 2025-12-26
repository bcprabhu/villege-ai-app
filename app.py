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

st.set_page_config(page_title="Village AI Super App", page_icon="🚜")

# --- SIDEBAR ---
st.sidebar.title("Settings")
language_choice = st.sidebar.selectbox(
    "Choose Language / भाषा",
    ("Hindi", "English", "Marathi", "Telugu", "Tamil", "Kannada", "Bengali")
)

# Location setting for Weather/Mandi
location = st.sidebar.text_input("Enter your Village/District:", value="Nagpur")

lang_codes = {"Hindi": "hi", "English": "en", "Marathi": "mr", "Telugu": "te", "Tamil": "ta", "Kannada": "kn", "Bengali": "bn"}

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

st.title("🚜 Village AI Super App")

# --- TABBED INTERFACE ---
tab1, tab2, tab3 = st.tabs(["💬 Ask AI", "📸 Plant Doctor", "📊 Mandi & Weather"])

with tab1:
    user_q = st.text_input("Ask a question:")
    if st.button("Get Answer"):
        if user_q:
            with st.spinner("Thinking..."):
                response = model.generate_content(f"Answer simply in {language_choice}: {user_q}")
                st.success(response.text)
                speak(response.text, lang_codes[language_choice])

with tab2:
    st.write("Take a photo of a sick plant.")
    img_file = st.camera_input("Take a Photo")
    if img_file:
        img = Image.open(img_file)
        if st.button("Identify Problem"):
            with st.spinner("Analyzing..."):
                response = model.generate_content([f"Identify the plant problem in this image and suggest a solution in {language_choice}.", img])
                st.success(response.text)
                speak(response.text, lang_codes[language_choice])

with tab3:
    st.header(f"Updates for {location}")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Check Mandi Bhav"):
            with st.spinner("Fetching prices..."):
                # Gemini searches its data for current trends
                prompt = f"Give a brief update on current market prices (Mandi Bhav) for major crops like Wheat, Rice, and Cotton in {location}. Answer in {language_choice}."
                response = model.generate_content(prompt)
                st.info(response.text)
    
    with col2:
        if st.button("Check Weather"):
            with st.spinner("Checking sky..."):
                prompt = f"Give a brief weather forecast for the next 2 days in {location}. Focus on if it's safe for sowing or harvesting. Answer in {language_choice}."
                response = model.generate_content(prompt)
                st.warning(response.text)

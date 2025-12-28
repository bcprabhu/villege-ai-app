import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
from PIL import Image
import urllib.parse
from streamlit_mic_recorder import mic_recorder # Import the recorder

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="Village AI Super App", page_icon="🚜", layout="wide")

# --- 2. LOGO LOADING ---
try:
    logo = Image.open("logo.jpg")
    st.sidebar.image(logo, use_container_width=True)
except Exception:
    st.sidebar.info("Upload logo.jpg to see the farmer image.")

# --- 3. SIDEBAR SETTINGS & CREATOR INFO ---
st.sidebar.title("Settings / ಸಂಯೋಜನೆಗಳು")
language_choice = st.sidebar.selectbox(
    "Choose Language / ಭಾಷೆಯನ್ನು ಆರಿಸಿ",
    ("Hindi", "English", "Marathi", "Telugu", "Tamil", "Kannada", "Bengali"),
    index=5
)
location = st.sidebar.text_input("Village/District (ಹಳ್ಳಿ/ಜಿಲ್ಲೆ):", value="Bengaluru")

st.sidebar.markdown("---")
st.sidebar.write("👨‍🏫 **Created By:**")
st.sidebar.write("**B.C. Prabhakar**")
st.sidebar.caption("Freelance Oil and Gas Engineering Consultant")

# --- WHATSAPP CONTACT BUTTON ---
phone_number = "91XXXXXXXXXX" # Update with your number
message = urllib.parse.quote("Hello Mr. Prabhakar, I am using your Village AI App.")
whatsapp_url = f"https://wa.me/{phone_number}?text={message}"
st.sidebar.link_button("💬 Chat with me on WhatsApp", whatsapp_url)

# --- 4. CONNECTIONS & LOGIC ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash') # Using 1.5 for better audio support
else:
    st.error("API Key missing!")

def speak(text, lang_code):
    try:
        lang_map = {"Hindi": "hi", "English": "en", "Marathi": "mr", "Telugu": "te", "Tamil": "ta", "Kannada": "kn", "Bengali": "bn"}
        tts = gTTS(text=text, lang=lang_map[language_choice])
        tts.save("voice.mp3")
        with open("voice.mp3", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except:
        pass

# --- 5. MAIN CONTENT ---
st.title("🚜 Village AI Super App")
st.subheader("Your Digital Farming Expert / ನಿಮ್ಮ ಕೃಷಿ ತಜ್ಞ")

# WE CREATE THE TABS FIRST
tab1, tab2, tab3 = st.tabs(["💬 Ask AI", "📸 Plant Doctor", "📊 Mandi & Weather"])

with tab1:
    st.write("Ask by Speaking or Typing (ಮಾತನಾಡಲು ಅಥವಾ ಟೈಪ್ ಮಾಡಿ):")
    
    # Voice Input
    audio = mic_recorder(
        start_prompt="🎤 Click to Speak (ಮಾತನಾಡಲು ಒತ್ತಿರಿ)",
        stop_prompt="🛑 Stop (ನಿಲ್ಲಿಸಿ)",
        key='recorder'
    )

    if audio:
        with st.spinner("Processing Voice..."):
            # Send audio bytes to Gemini
            audio_data = {"mime_type": "audio/wav", "data": audio['bytes']}
            response = model.generate_content([
                f"The user is a farmer speaking in {language_choice}. Identify their question and answer clearly in {language_choice}.",
                audio_data
            ])
            st.success(response.text)
            speak(response.text, language_choice)
            st.download_button("📥 Download Report", response.text, file_name="advice.txt")

    st.markdown("---")
    
    # Typing Option
    user_q = st.text_input("Or type your question here:")
    if st.button("Get Answer", key="q_btn"):
        if user_q:
            with st.spinner("Thinking..."):
                response = model.generate_content(f"Answer simply in {language_choice}: {user_q}")
                st.success(response.text)
                speak(response.text, language_choice)
                st.download_button("📥 Download Report", response.text, file_name="advice.txt")

# --- THE REST OF THE TABS (NO CHANGES NEEDED HERE) ---
with tab2:
    st.write("Upload or take a photo of a crop problem.")
    img_file = st.camera_input("Capture Crop Image")
    if img_file:
        img = Image.open(img_file)
        if st.button("Analyze Plant"):
            with st.spinner("Analyzing..."):
                response = model.generate_content([f"Identify the plant problem in this image and suggest a solution in {language_choice}.", img])
                st.success(response.text)
                speak(response.text, language_choice)
                st.download_button("📥 Download Health Report", response.text, file_name="plant_report.txt")

with tab3:
    st.header(f"Live Updates: {location}")
    if st.button("Get Mandi & Weather Updates"):
        with st.spinner("Fetching..."):
            response = model.generate_content(f"Give crop prices and weather for {location} in {language_choice}.")
            st.info(response.text)

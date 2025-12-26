import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
from PIL import Image

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="Village AI Super App", page_icon="🚜", layout="wide")

# --- 2. LOGO LOADING ---
try:
    logo = Image.open("logo.jpg")
    st.sidebar.image(logo, use_container_width=True)
except Exception:
    st.sidebar.warning("Logo 'logo.jpg' not found.")

# --- 3. SETTINGS & CONNECTIONS ---
st.sidebar.title("Settings / ಸಂಯೋಜನೆಗಳು")

# Defaulting to Kannada (index 5)
language_choice = st.sidebar.selectbox(
    "Choose Language / ಭಾಷೆಯನ್ನು ಆರಿಸಿ",
    ("Hindi", "English", "Marathi", "Telugu", "Tamil", "Kannada", "Bengali"),
    index=5
)

location = st.sidebar.text_input("Village/District (ಹಳ್ಳಿ/ಜಿಲ್ಲೆ):", value="Bengaluru")

# --- 4. FEEDBACK SECTION ---
st.sidebar.markdown("---")
st.sidebar.subheader("Feedback / ಪ್ರತಿಕ್ರಿಯೆ")
rating = st.sidebar.feedback("stars")
if rating is not None:
    st.sidebar.write(f"Thank you for the {rating + 1} star rating!")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
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
st.write("Welcome to your digital farming expert. / ನಿಮ್ಮ ಡಿಜಿಟಲ್ ಕೃಷಿ ತಜ್ಞರಿಗೆ ಸ್ವಾಗತ.")

# Simple Instructions
with st.expander("📖 How to use this App / ಈ ಆಪ್ ಅನ್ನು ಹೇಗೆ ಬಳಸುವುದು"):
    st.write("""
    1. **Ask AI**: Type any farming question. / ನಿಮ್ಮ ಕೃಷಿ ಪ್ರಶ್ನೆಯನ್ನು ಟೈಪ್ ಮಾಡಿ.
    2. **Plant Doctor**: Take a photo of a sick leaf. / ರೋಗಪೀಡಿತ ಎಲೆಯ ಫೋಟೋ ತೆಗೆದುಕೊಳ್ಳಿ.
    3. **Mandi & Weather**: Check prices and rain. / ಬೆಲೆಗಳು ಮತ್ತು ಮಳೆಯನ್ನು ಪರಿಶೀಲಿಸಿ.
    """)

tab1, tab2, tab3 = st.tabs(["💬 Ask AI", "📸 Plant Doctor", "📊 Mandi & Weather"])

with tab1:
    user_q = st.text_input("Ask a question:")
    if st.button("Get Answer"):
        if user_q:
            with st.spinner("Thinking..."):
                response = model.generate_content(f"Answer simply in {language_choice}: {user_q}")
                st.success(response.text)
                speak(response.text, language_choice)

with tab2:
    st.write("Take a photo of a leaf or pest.")
    img_file = st.camera_input("Capture")
    if img_file:
        img = Image.open(img_file)
        if st.button("Identify"):
            with st.spinner("Analyzing..."):
                response = model.generate_content([f"Identify the plant problem in this image and suggest a solution in {language_choice}.", img])
                st.success(response.text)
                speak(response.text, language_choice)

with tab3:
    st.header(f"Updates for {location}")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Mandi Bhav"):
            response = model.generate_content(f"Give crop prices for {location} in {language_choice}.")
            st.info(response.text)
    with c2:
        if st.button("Weather"):
            response = model.generate_content(f"Give weather for {location} in {language_choice}.")
            st.warning(response.text)

import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64
from PIL import Image
import urllib.parse

# --- 1. SET PAGE CONFIG ---
st.set_page_config(page_title="Village AI Super App", page_icon="🚜", layout="wide")

# --- 2. LOGO LOADING ---
try:
    logo = Image.open("logo.jpg")
    st.sidebar.image(logo, use_container_width=True)
except Exception:
    st.sidebar.info("Upload logo.jpg as farmer logo if you want to see an image here.")

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
phone_number = "91XXXXXXXXXX"  # <-- put your full WhatsApp number here
message = urllib.parse.quote("Hello Mr. Prabhakar, I am using your Village AI App.")
whatsapp_url = f"https://wa.me/{phone_number}?text={message}"
st.sidebar.link_button("💬 Chat with me on WhatsApp", whatsapp_url)

# --- 4. GEMINI CONNECTION & MODEL ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.error("API Key missing in Secrets! Please add GEMINI_API_KEY in Streamlit Cloud.")
    st.stop()

# --- 5. TEXT TO SPEECH HELPER ---
def speak(text: str, language_label: str):
    """Convert text to speech and auto‑play in browser."""
    try:
        lang_map = {
            "Hindi": "hi",
            "English": "en",
            "Marathi": "mr",
            "Telugu": "te",
            "Tamil": "ta",
            "Kannada": "kn",
            "Bengali": "bn",
        }
        lang_code = lang_map.get(language_label, "en")
        tts = gTTS(text=text, lang=lang_code)
        tts.save("voice.mp3")

        with open("voice.mp3", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()

        # Note: Some browsers block autoplay; user may need to click play. [web:28]
        audio_html = f"""
        <audio controls autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Speaker not available now: {str(e)[:80]}")

# --- 6. MAIN CONTENT ---
st.title("🚜 Village AI Super App")
st.subheader("Your Digital Farming Expert / ನಿಮ್ಮ ಕೃಷಿ ತಜ್ಞ")

tab1, tab2, tab3 = st.tabs(["💬 Ask AI", "📸 Plant Doctor", "📊 Mandi & Weather"])

# ---------- TAB 1: VOICE + TEXT ----------
with tab1:
    st.write("### 🎤 Speak Your Question / ಮಾತನಾಡಿ")

    # Audio input from microphone (Streamlit >= 1.29). [web:16][web:17]
    audio_file = st.audio_input("Tap the mic and speak (3–5 seconds)")

    if audio_file:
        with st.spinner("Analyzing your voice..."):
            try:
                audio_bytes = audio_file.read()

                # Gemini expects a list of parts: audio + text instruction. [web:21]
                audio_parts = [
                    {
                        "mime_type": "audio/mp3",   # Streamlit mic gives webm/ogg/mp3; mp3 works well. [web:21]
                        "data": audio_bytes,
                    },
                    f"You are a farming expert. Listen to this audio and answer clearly in {language_choice}.",
                ]

                response = model.generate_content(audio_parts)
                answer = getattr(response, "text", "").strip()

                if answer:
                    st.success(answer)
                    speak(answer, language_choice)
                else:
                    st.info("No answer came from the model. Please try again with a shorter question.")
            except Exception as e:
                st.error(f"Voice Error: {str(e)[:150]}")
                st.info("Try a short 3–5 second recording, or use the quick buttons / typing below.")

    st.markdown("---")
    st.write("### Quick Help / ತ್ವರಿತ ಸಹಾಯ")

    col1, col2 = st.columns(2)
    query = ""

    with col1:
        if st.button("🌾 Rice/Paddy Tips"):
            query = "Give me 5 important tips for high yield in Paddy farming."
        if st.button("🍅 Tomato Diseases"):
            query = "What are the common diseases in Tomato and how to cure them?"
        if st.button("🐛 Pest Control"):
            query = "Suggest low-cost organic ways to control pests in the field."

    with col2:
        if st.button("💧 Save Water"):
            query = "What are the best irrigation methods to save water for a small farmer?"
        if st.button("🌱 Organic Fertilizer"):
            query = "How to make high-quality organic fertilizer at home?"
        if st.button("💰 Govt Schemes"):
            query = "Tell me about top 3 government schemes for small farmers in India."

    st.markdown("---")

    user_q = st.text_input("Or type here (ಅಥವಾ ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ):", value=query)

    if st.button("Get Answer", key="q_btn"):
        if user_q.strip():
            with st.spinner("Thinking..."):
                response = model.generate_content(
                    f"Answer this for a small farmer in simple language in {language_choice}: {user_q}"
                )
                answer = getattr(response, "text", "").strip()
                if answer:
                    st.success(answer)
                    speak(answer, language_choice)
                else:
                    st.info("Model did not return any answer. Please try a different question.")
        else:
            st.warning("Please type a question or use one of the ready buttons.")

# ---------- TAB 2: PLANT DOCTOR ----------
with tab2:
    st.write("### 📸 Plant Doctor")
    img_file = st.camera_input("Capture Crop Image")

    if img_file:
        img = Image.open(img_file)
        if st.button("Analyze Plant"):
            with st.spinner("Analyzing..."):
                response = model.generate_content(
                    [
                        f"Identify the plant problem in this image and suggest a simple solution in {language_choice}.",
                        img,
                    ]
                )
                answer = getattr(response, "text", "").strip()
                if answer:
                    st.success(answer)
                    speak(answer, language_choice)
                else:
                    st.info("Could not understand the image. Try a clearer photo of leaves or affected area.")

# ---------- TAB 3: MANDI & WEATHER ----------
with tab3:
    st.write("### 📊 Mandi & Weather")
    st.header(f"Updates for: {location}")

    if st.button("Get Live Updates"):
        with st.spinner("Fetching..."):
            response = model.generate_content(
                f"Give current crop prices and 2-day weather for {location} in {language_choice}. "
                f"Be clear and farmer-friendly."
            )
            info_text = getattr(response, "text", "").strip()
            if info_text:
                st.info(info_text)
            else:
                st.info("No update received. Please try again or check your API quota.")

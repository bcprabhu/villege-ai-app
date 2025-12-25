import streamlit as st
from gtts import gTTS
import base64

# Page styling
st.set_page_config(page_title="Village AI", page_icon="🌾")
st.title("🌾 Village AI Smart Assistant")
st.header("ग्रामीण एआई स्मार्ट सहायक")

# A simple "Knowledge Brain" for the village
knowledge_base = {
    "water": "नदियों और तालाबों को साफ रखें। वर्षा जल संचयन (Rainwater harvesting) अपनाएं।",
    "crop": "मिट्टी की जांच कराएं और जैविक खाद का उपयोग करें।",
    "health": "साफ पानी पिएं और अपने आसपास स्वच्छता बनाए रखें।",
    "default": "यह एक बहुत अच्छा प्रश्न है। हमें इसके बारे में और विस्तार से चर्चा करनी चाहिए।"
}

# 1. User Input
user_query = st.text_input("Ask about crops, water, or health / खेती, पानी या स्वास्थ्य के बारे में पूछें:")

# 2. Voice Function
def speak(text):
    tts = gTTS(text=text, lang='hi')
    tts.save("response.mp3")
    with open("response.mp3", "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    audio_html = f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
    st.markdown(audio_html, unsafe_allow_html=True)

# 3. Smart Logic
if st.button('Get Expert Advice / सलाह प्राप्त करें'):
    if user_query:
        # Simple keyword matching to simulate an AI brain
        query_lower = user_query.lower()
        if "पानी" in query_lower or "water" in query_lower:
            answer = knowledge_base["water"]
        elif "खेती" in query_lower or "crop" in query_lower:
            answer = knowledge_base["crop"]
        elif "स्वास्थ्य" in query_lower or "health" in query_lower:
            answer = knowledge_base["health"]
        else:
            answer = knowledge_base["default"]
            
        st.success(f"AI: {answer}")
        speak(answer)
    else:
        st.warning("Please type a question! / कृपया प्रश्न लिखें!")

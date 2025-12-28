from streamlit_mic_recorder import mic_recorder

with tab1:
    st.write("Ask by Typing or Speaking (ಟೈಪ್ ಮಾಡಿ ಅಥವಾ ಧ್ವನಿ ಮೂಲಕ ಕೇಳಿ):")
    
    # 1. Voice Input Option
    audio = mic_recorder(
        start_prompt="🎤 Click to Speak (ಮಾತನಾಡಲು ಒತ್ತಿರಿ)",
        stop_prompt="🛑 Stop (ನಿಲ್ಲಿಸಿ)",
        key='recorder'
    )

    # 2. Typing Option
    user_q = st.text_input("Or type here (ಅಥವಾ ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ):")

    if audio:
        # This sends the audio to Gemini to 'transcribe' and answer
        with st.spinner("Listening..."):
            response = model.generate_content([f"The user is speaking in {language_choice}. Please transcribe and answer their question.", audio['bytes']])
            st.success(response.text)
            speak(response.text, language_choice)
    
    elif st.button("Get Answer"):
        if user_q:
            with st.spinner("Thinking..."):
                response = model.generate_content(f"Answer simply in {language_choice}: {user_q}")
                st.success(response.text)
                speak(response.text, language_choice)

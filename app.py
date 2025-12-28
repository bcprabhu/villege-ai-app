with tab1:
    st.write("### Ask a Question / ಪ್ರಶ್ನೆ ಕೇಳಿ")
    
    # Using the standard audio input - much more stable for mobile!
    audio_file = st.audio_input("Record your question (ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ರೆಕಾರ್ಡ್ ಮಾಡಿ)")

    if audio_file:
        with st.spinner("Analyzing your voice..."):
            # Gemini 'listens' to the file directly
            response = model.generate_content([
                f"The user is a farmer speaking in {language_choice}. Please transcribe their question and provide a helpful answer in {language_choice}.",
                {"mime_type": "audio/wav", "data": audio_file.getvalue()}
            ])
            st.success(response.text)
            speak(response.text, language_choice)
            st.download_button("📥 Download Report", response.text, file_name="voice_advice.txt")

    st.markdown("---")
    user_q = st.text_input("Or type here (ಅಥವಾ ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ):")
    if st.button("Get Answer", key="q_btn"):
        if user_q:
            with st.spinner("Thinking..."):
                response = model.generate_content(f"Answer simply in {language_choice}: {user_q}")
                st.success(response.text)
                speak(response.text, language_choice)

# --- SIDEBAR LOGO ---
try:
    logo_img = Image.open("logo.jpg")
    st.sidebar.image(logo_img, caption="Expert Guidance for Farmers", use_container_width=True)
except Exception as e:
    st.sidebar.info("Upload logo.jpg to GitHub to see your logo here!")

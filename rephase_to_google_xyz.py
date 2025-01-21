import streamlit as st
import google.generativeai as genai

def rephase_to_google_xyz_page(api_key, model_name):
    st.title("📄 Rephase to Google Recruiter XYZ formula")
    
    # Bullet point input
    bullet_point = st.text_area("Paste the bullet point here")
    
    if st.button("Rephase"):
        if bullet_point and model_name:
            with st.spinner("Analyzing..."):
                # Set your Google Generative AI API key
                genai.configure(api_key=api_key)
                # Send to Google Generative AI for matching score
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    f"Please rephrase the following bullet point, incorporate quantifiable achievements and improvements, following the Google recruiter XYZ formula. Give each suggested bullet point response below 40 words. Ensure the bullet points optimized for ATS screening.Below is my bullet point to extract relevent information:\n{bullet_point}"
                )
                st.write("Rephrased Bullet Point:\n", response.text)
import streamlit as st
import google.generativeai as genai

def core_competencies_extractor_page(api_key, model_name, job_description):
    st.title("📄 Core competencies extractor")
    
    if st.button("Extract"):
        if job_description and model_name:
            with st.spinner("Analyzing..."):
                # Set your Google Generative AI API key
                genai.configure(api_key=api_key)
                # Send to Google Generative AI for matching score
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    f"please give me 6 important core competencies from Job Description:\n{job_description}\nPlease explain the core competencies. and then please provide the core competencies separate by |"
                )
                st.write("Core competencies:\n\n", response.text)
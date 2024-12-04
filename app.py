import streamlit as st
import PyPDF2
import google.generativeai as genai

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Make Streamlit page wide
st.set_page_config(page_title="ATS Resume Evaluation System", layout="wide")

# API Key Input (Password Field)
api_key = st.text_input("Enter your Google Generative AI API key", type="password")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Rephase to Google XYZ", "Bullet Point Rephaser", "Resume Generator"])

if page == "Rephase to Google XYZ":
    st.title("📄 Rephase to Google Recruiter XYZ formula")
    
    # Bullet point input
    bullet_point = st.text_area("Paste the bullet point here")
    
    if st.button("Rephase"):
        if bullet_point:
            with st.spinner("Analyzing..."):
                # Set your Google Generative AI API key
                genai.configure(api_key=api_key)
                # Send to Google Generative AI for matching score
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(
                    f"Rewrite these bullet point using this structure: 'Accomplished [X] as measured by [Y], by doing [Z]' format, highlighting the 'what' (X), 'how it was measured'(Y), and 'specific actions taken' (Z) to showcase the impact of your work with quantifiable data, use compelling language, without buzzwords and keep it under 200 words, give me 3 variations for each bullet point, Do not explain the 'Accomplished, measured, and by doing' phrases, the order of in sentence for the X,Y,Z can be different so that it is more engaging, measured by can be ignore if it is not applicable. Z should start with powerful action verbs, do not use first person. Just need to provide the rephase sentence. Below is my bullet point to extract relevent information:\n{bullet_point}"
                )
                st.write("Rephrased Bullet Point:\n", response.text)

if page == "Bullet Point Rephaser":
    st.title("📄 ATS Bullet Point Rephaser")

elif page == "Resume Generator":
    st.title("📝 ATS Resume Generator")

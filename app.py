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
page = st.sidebar.radio("Go to", ["Rephase to Google XYZ", "Core competencies extractor", "Bullet Point Rephaser", "Resume Generator"])

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
                    f"Please rephrase the following bullet point, incorporate quantifiable achievements and improvements, following the Google recruiter XYZ formula. Give each suggested bullet point response below 40 words. Ensure the bullet points optimized for ATS screening.Below is my bullet point to extract relevent information:\n{bullet_point}"
                )
                st.write("Rephrased Bullet Point:\n", response.text)
                
if page == "Core competencies extractor":
    st.title("📄 Core competencies extractor")
    
    # Job description input
    job_description = st.text_area("Paste the job description here")
    
    if st.button("Extract"):
        if job_description:
            with st.spinner("Analyzing..."):
                # Set your Google Generative AI API key
                genai.configure(api_key=api_key)
                # Send to Google Generative AI for matching score
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(
                    f"please give me 6 important core competencies from Job Description:\n{job_description}\nPlease explain the core competencies. and then please provide the core competencies separate by |"
                )
                st.write("Core competencies:\n\n", response.text)

if page == "Bullet Point Rephaser":
    st.title("📄 ATS Bullet Point Rephaser")
    
    # Job title input
    job_title = st.text_input("Paste the job title here")
    
    # Job description input
    job_description = st.text_area("Paste the job description here")

    # Bullet point input
    bullet_point = st.text_area("Paste the bullet point here")
    
    if st.button("Find keywords"):
        if job_description:
            with st.spinner("Analyzing..."):
                # Set your Google Generative AI API key
                genai.configure(api_key=api_key)
                # Send to Google Generative AI for matching score
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(
                    f"You are a highly skilled ATS (Applicant Tracking System) scanner with expert-level knowledge of ATS standards and functionality. Your task is to extract and list only the most relevant keywords from the provided job description. Ensure that each keyword aligns precisely with the job title and its core requirements. Be concise, accurate, and provide the keyword per line end separate by comma without any additional explanations or irrelevant terms. Do not generate or fabricate any content beyond what is present in the job description.\n\nJob title:{job_title}\n\nJob description:{job_description}"
                )
                #st.write(response.text)
                
                response_rephase = model.generate_content(
                    f"Please rephrase the following bullet point using the suggested keywords and incorporate quantifiable achievements and improvements, following the Google recruiter XYZ formula. Ensure the bullet points remain precise, concise, and optimized for ATS screening. Focus exclusively on bullet points without adding any new or fabricated information, give each suggested bullet point response below 40 words.\n\nBullet point:\n{bullet_point}\n\nSuggestions:\n{response.text}"
                )
                st.write("Keywords:\n", response.text)
                st.write("\nRephrased Bullet Point:\n", response_rephase.text)

elif page == "Resume Generator":
    st.title("📝 ATS Resume Generator")

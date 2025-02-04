import streamlit as st
import google.generativeai as genai
from groq import Groq
from utils import extract_text_from_pdf, generate_speech
from rephase_to_google_xyz import rephase_to_google_xyz_page
from core_competencies_extractor import core_competencies_extractor_page
from bullet_point_rephaser import bullet_point_rephaser_page
from ats_friendly_resume_generator import ats_friendly_resume_generator_page
from generate_cover_letter import generate_cover_letter_page
from introduction_generator import introduction_generator_page
from tell_me_about_yourself import tell_me_about_yourself_page
from top_interview_questions import top_interview_questions_page
from common_interview_questions import common_interview_questions_page

# Make Streamlit page wide
st.set_page_config(page_title="ATS Resume Evaluation System", layout="wide")

# Function to fetch Groq models
def fetch_groq_models(api_key):
    try:
        client = Groq(api_key=api_key)
        models = client.models.list().data
        return [model.id for model in models]
    except Exception as e:
        st.error(f"Error fetching Groq models: {e}")
        return []

# Create two columns for API key and model selection
col1, col2 = st.columns(2)

# API Key Input (Password Field) in the first column
with col1:
    api_key = st.text_input("Enter your Google Generative AI API key", type="password")

# Model provider selection dropdown in the second column
with col2:
    model_provider = st.selectbox("Select Model Provider", ["Gemini", "Groq"])
    if model_provider == "Gemini":
        if api_key:
            genai.configure(api_key=api_key)
            model_list = [model.name for model in genai.list_models() if 'gemini' in model.name]
            model_name = st.selectbox("Select Gemini Model", model_list)
        else:
            model_name = None
            st.warning("Please enter your API key to select a model.")
    elif model_provider == "Groq":
        if api_key:
            if "groq_models" not in st.session_state:
                st.session_state.groq_models = fetch_groq_models(api_key)
            model_name = st.selectbox("Select Groq Model", st.session_state.groq_models)
        else:
            model_name = None
            st.warning("Please enter your API key to select a model.")
    else:
        model_name = None


# Job title input
job_title = st.text_input("Paste the job title here")

# Job description input
job_description = st.text_area("Paste the job description here")

# File uploader
uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Rephase to Google XYZ", "Core competencies extractor", "Bullet Point Rephaser", "ATS Friendly Resume Generator", "Generate Cover Letter", "Introduction Generator", "Tell me about yourself", "Top Interview Questions", "Common Interview Questions"])

if page == "Rephase to Google XYZ":
    rephase_to_google_xyz_page(api_key, model_name, model_provider)
elif page == "Core competencies extractor":
    core_competencies_extractor_page(api_key, model_name, model_provider, job_description)
elif page == "Bullet Point Rephaser":
    bullet_point_rephaser_page(api_key, model_name, model_provider, job_title, job_description)
elif page == "ATS Friendly Resume Generator":
    ats_friendly_resume_generator_page(api_key, model_name, model_provider, uploaded_file, job_description)
elif page == "Generate Cover Letter":
    generate_cover_letter_page(api_key, model_name, model_provider, uploaded_file, job_title, job_description)
elif page == "Introduction Generator":
    introduction_generator_page(api_key, model_name, model_provider, uploaded_file, job_title, job_description)
elif page == "Tell me about yourself":
    tell_me_about_yourself_page(api_key, model_name, model_provider, uploaded_file, job_title, job_description)
elif page == "Top Interview Questions":
    top_interview_questions_page(api_key, model_name, model_provider, job_description, uploaded_file, page)
elif page == "Common Interview Questions":
    common_interview_questions_page(api_key, model_name, model_provider, job_description, uploaded_file)

st.sidebar.markdown("---")
st.sidebar.markdown("© 2024 khawslee. All rights reserved.")

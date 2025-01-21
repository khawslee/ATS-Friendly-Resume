import streamlit as st
import google.generativeai as genai
from utils import extract_text_from_pdf

def top_interview_questions_page(api_key, model_name, job_description, uploaded_file, typeofQuestion):
    st.title("Top 5 Interview Questions")
    typeofQuestion = st.selectbox("Type of questions", ["Behaviour", "Technical"])
    
    if st.button("Generate Questions and Answers"):
        if job_description and model_name and api_key and uploaded_file:
            with st.spinner("Generating..."):
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name)
                resume_text = extract_text_from_pdf(uploaded_file)
                prompt = f"""
                    You are an expert career assistant specializing in crafting compelling interview questions and answers.
                    
                    Task:
                    - Generate the top 5 most {typeofQuestion} interview questions that an interviewer would ask for the given job description and resume.
                    - Provide a concise and professional answer for each question, tailored to the job description and resume.
                    
                    Guidelines:
                    - The questions should be relevant to the job description and the candidate's resume.
                    - The answers should be concise, professional, and highlight the candidate's strengths and qualifications, utilizing CARL method Context, Action, Result, Learning.
                    - Each answer should be no more 2 minutes.
                    - The output should be in a clear and easy-to-read format.
                    
                    Inputs:
                    Job Description: {job_description}
                    Resume: {resume_text}
                    
                    Output:
                    Provide the questions and answers in the following format:
                    Question: [Question]
                    Answer: [Answer]
                    """
                response = model.generate_content(prompt)
                st.write(response.text)
        else:
            st.warning("Please enter job description, resume, API key and select a model.")
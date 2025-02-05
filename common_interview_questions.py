import streamlit as st
import google.generativeai as genai
from utils import extract_text_from_pdf
import groq

def common_interview_questions_page(api_key, model_name, model_provider, job_description, uploaded_file):
    st.title("Common Interview Questions")
    
    #List of questions
    listofQuestion = ["What makes you unique?", "Tell me about yourself and your qualifications.", "Why do you want to work at this company?", "What interests you about this role?", "What motivates you?", "What are your greatest strengths?", "What are your greatest weaknesses?", "What are your goals for the future?", "Where do you think you'll be in five years?", "What did you like most about your last position?", "What did you like least about your last position?", "Can you tell me about a difficult work situation and how you overcame it?", "How do you respond to stress or change?", "How do you handle conflict at work?", "What is your greatest accomplishment?", "How do you define success?", "How do your skills align with this role?", "Why should we hire you?", "Why are you leaving your current job?", "What is your salary range expectation?", "Do you have any questions?", "What are you passionate about?", "What is your teaching philosophy?", "What does customer service mean to you?", "Tell me about your work experience.", "How do you work under pressure?", "What is your dream job?", "What can you bring to the company?"]
    
    if st.button("Generate Questions and Answers"):
        if job_description and model_name and api_key and uploaded_file:
            with st.spinner("Generating..."):
                resume_text = extract_text_from_pdf(uploaded_file)
                if model_provider == "Gemini":
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(model_name)
                    prompt = f"""
                        You are an expert career assistant specializing in crafting compelling interview questions and answers.
                        
                        Task:
                        - Provide a concise and professional answer for each question listed in {listofQuestion}, tailored to the job description and resume.
                        
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
                elif model_provider == "Groq":
                    client = groq.Groq(api_key=api_key)
                    chat_completion = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {
                                "role": "user",
                                "content": f"""
                                    You are an expert career assistant specializing in crafting compelling interview questions and answers.
                                    
                                    Task:
                                    - Provide a concise and professional answer for each question listed in {listofQuestion}, tailored to the job description and resume.
                                    
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
                                    """,
                            }
                        ],
                    )
                    st.write(chat_completion.choices[0].message.content)
                    return
                prompt = f"""
                    You are an expert career assistant specializing in crafting compelling interview questions and answers.
                    
                    Task:
                    - Provide a concise and professional answer for each question listed in {listofQuestion}, tailored to the job description and resume.
                    
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
import streamlit as st
import google.generativeai as genai
from utils import extract_text_from_pdf, generate_speech

def introduction_generator_page(api_key, model_name, uploaded_file, job_title, job_description):
    st.title("Introduction Generator")
    
    resume_text = extract_text_from_pdf(uploaded_file)

    if st.button("Generate Introduction"):
        if job_title and job_description and resume_text and model_name and api_key:
            with st.spinner("Generating..."):
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name)
                
                prompt = """
					You are an expert career assistant specializing in crafting compelling introductions about yourself. Perform the following tasks step-by-step:

					- Analyze and Summarize Challenges: Carefully read the provided job description and identify the biggest day-to-day challenge someone in the role would face and the pain points of the company for this job role. Write the summary in a concise and professional tone.
					- Create an Attention-Grabbing Hook: Based on the summarized challenge, write a captivating opening sentence or hook that highlights how a candidate with the right skills can overcome this challenge.
					- Draft a interview answer: Using the hook from Step 2 as the opening paragraph, write a professional interview answer about yourself tailored to the job description.
                    
                    Guidelines:
                    - Align the introduction with the specific job description, incorporating relevant keywords, essential skills, and qualifications from the provided resume.
                    - Demonstrate how the candidate's experience, accomplishments, and skills make them the ideal fit for the role.
                    - Keep the tone professional and engaging, expressing enthusiasm for the role and the company.
                    - The introduction must be concise in less than 2 minutes with a clear structure:
                    - Opening Paragraph: Thank for interview opportunity then introduce yourself then use the hook from Step 2.
                    - Body Paragraph(s): Showcase only relevant skills, achievements which with the company’s needs with measurable matric.
                    - Closing Paragraph: Reiterate interest, express excitement to contribute, and include a call to action for the next steps.
                    - Avoid repetition and ensure every sentence adds value, demonstrating expertise in crafting impactful introduction.
                    Generate a final output that is polished, and tailored for maximum impact.
                    Keep each paragraph is within 50 words, easy to read, short and consise, do not repeat too much from the resume and the introduction is about what I can bring value to the company, and the output is more conversation style and easy for the recruiter to understand.
					
					Inputs:
                    Job Title: {job_title}
					Job Description: {job_description}.
					Resume: {resume_text}.
					
					Output:
					Only the introduction in plain text format in paragraphs, do not provide breakdown
                    """
                    
                response = model.generate_content(
                    prompt.format(job_title=job_title, job_description=job_description, resume_text=resume_text)
                )
                # f"Please generate a self-introduction and experience summary not more than 2 minutes for a recruiter based on the following job title, job description, and resume. Start by thanking for the intervie opportunity, then introduce yourself, after that craft an attention grabbing hook based on the summarized challenges, then continue with the present and tell why you are well qualified for the position, matching your qualifications to what the recruiter is looking for. Keep it short, simple, and in the end include a call to action for the next steps. Provide the output as plain text with easy to read format, and the introduction should be like in a interview. \n\nJob Title: {job_title}\nJob Description: {job_description}\nResume: {resume_text}"
                introduction_text = response.text
                st.write(introduction_text)

                # Generate speech
                audio_file = generate_speech(introduction_text, "introduction.wav")
                if audio_file:
                    # Play audio in Streamlit
                    st.audio(audio_file)
        else:
            st.warning("Please enter job title, job description, resume, API key and select a model.")
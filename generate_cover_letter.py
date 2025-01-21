import streamlit as st
import google.generativeai as genai
from utils import extract_text_from_pdf

def generate_cover_letter_page(api_key, model_name, uploaded_file, job_title, job_description):
    st.title("📝 ATS Friendly Cover Letter Generator")
    
    prompt_option = st.selectbox("Select a prompt", ["Short", "Long"])

    if st.button("Generate Cover Letter"):
        if uploaded_file and model_name:
            with st.spinner("Analyzing..."):
                # Set your Google Generative AI API key
                genai.configure(api_key=api_key)
                resume_text = extract_text_from_pdf(uploaded_file)
                # Send to Google Generative AI for matching score
                model = genai.GenerativeModel(model_name)
                
                prompt1 = """
					You are a career coach specializing in creating concise and impactful short cover letters. Your goal is to craft a polished response that aligns with the job description and the candidate's resume, ensuring maximum relevance and engagement in a brief format. Follow these steps carefully:
                    
                    Guidelines:
                    Step 1: Analyze Challenges
                    Review the job description to identify the key challenge or primary goal for the role. Summarize this in one sentence, focusing on what the company seeks to address with this hire.
                    Step 2: Draft the Short Cover Letter
                    Use the following structure to keep the letter concise (150–200 words):

                    Opening Paragraph:
                    Start with a warm thank-you for the opportunity.
                    Mention the job title and express enthusiasm for the role.
                    Briefly introduce the candidate’s background and how it aligns with the company’s needs.

                    Body Paragraph:
                    Highlight up to 2–3 key skills or achievements directly tied to the job description.
                    Focus on measurable results or experiences that showcase how the candidate can address the company’s primary challenge.
                    Write in plain text and use simple sentences for readability.

                    Closing Paragraph:
                    Reiterate excitement for contributing to the team.
                    Include a polite call to action (e.g., “I would love the opportunity to discuss how I can add value to your team in person.”).

                    Tone:
                    Professional yet conversational to engage the reader.
                    Use simple and clear English for easy understanding.
                    Avoid repetition or unnecessary details; focus on value and relevance.
                    Format:

                    Ensure the cover letter is no longer than 150–200 words.
                    Use keywords from the job description for ATS compatibility.
                    Focus on the candidate’s value to the company rather than restating the resume.

                    Inputs:
                    Job Title: {job_title}
                    Job Description: {job_description}
                    Resume: {resume_text}

                    Output:
                    Provide the short cover letter in plain text format, structured as described. Avoid additional steps or sections and focus solely on delivering the concise cover letter.

                    This revised prompt ensures the cover letter is impactful, concise, and tailored, ideal for situations where brevity is essential.
                    """
                
                prompt2 = """
                    You are a career coach specializing in crafting tailored, impactful, and professional cover letters. Your goal is to create a polished response that aligns with the job description and the candidate's resume, ensuring maximum engagement and relevance. Follow these steps carefully:

                    Guidelines:
                    Step 1: Analyze Challenges
                    Review the job description to identify key challenges, priorities, or opportunities specific to the role. Summarize this analysis concisely, highlighting what the company needs in this hire.
                    Step 2: Attention-Grabbing Hook
                    Based on the identified challenges, create a captivating opening sentence that demonstrates how the candidate’s expertise and experience align with the role’s requirements. This hook will serve as the opening for the cover letter.
                    Step 3: Draft the Cover Letter
                    Use the following structure to craft a concise, one-page cover letter:

                    Opening Paragraph:
                    Use the hook from Step 2 to introduce the candidate and express enthusiasm for the role.
                    Briefly mention how the candidate’s background makes them a great fit for solving key challenges.
                    
                    Body Paragraph(s):
                    Highlight Core Skills and Achievements: Start with: "I am experienced in the number of key areas relevant to this role. These are:"
                    Use a numbered bullet format to list up to 3 measurable accomplishments or skills from the resume that address the job description’s top priorities.

                    Ensure the listed skills are specific, measurable, and directly tied to the role’s requirements.
                    Each point should fit within a single line for readability.
                    Fit for the Role: Emphasize how these skills uniquely position the candidate to solve the company’s challenges and make an impact. If applicable, briefly explain why the candidate’s background is a strong fit despite any unconventional aspects.

                    Closing Paragraph:
                    Reiterate enthusiasm for the opportunity and how the candidate will contribute to the company’s success.
                    Include a polite call to action (e.g., "I look forward to discussing how my skills can contribute to your team.")
                    
                    Tone:
                    Professional yet conversational to maintain engagement.
                    Use simple, clear English for easy comprehension.
                    Avoid repetition or vague statements; every sentence should add value.

                    Format:
                    Each paragraph should be under 50 words for clarity.
                    Ensure ATS compatibility by including keywords from the job description and resume.
                    Focus on the value the candidate brings to the company, not on restating the resume.

                    Inputs:
                    Job Title: {job_title}
                    Job Description: {job_description}
                    Resume: {resume_text}
                    Output:
                    Generate the following:
                    Step 1: Challenge Summary – A concise summary of the role's challenges.
                    Step 2: Hook – An engaging opening sentence aligned with the challenge summary.
                    Step 3: Cover Letter – A polished, structured cover letter based on the provided guidelines.
                    
                    Ensure the final output is ATS-friendly, impactful, and clearly demonstrates the candidate's value to the company.
                    """
                
                prompt = prompt1 if prompt_option == "Short" else prompt2
                response = model.generate_content(
                    prompt.format(job_title=job_title, job_description=job_description, resume_text=resume_text)
                )
                st.write("Cover letter:\n", response.text)
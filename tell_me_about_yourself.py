import streamlit as st
import google.generativeai as genai
from utils import extract_text_from_pdf, generate_speech

def tell_me_about_yourself_page(api_key, model_name, model_provider, uploaded_file, job_title, job_description):
    st.title("Tell me about yourself")
    
    resume_text = extract_text_from_pdf(uploaded_file)

    if st.button("Generate"):
        if job_title and job_description and resume_text and model_name and api_key:
            with st.spinner("Generating..."):
                prompt = """
					You are a career coach with expertise in crafting impactful "Tell me about yourself" introductions for job interviews. Your goal is to create a polished and tailored response that aligns with the job description and the candidate's resume, ensuring maximum engagement and relevance. Follow these steps carefully:

                    Guidelines:
                    Introduction: Begin with a warm thank-you for the opportunity, followed by a concise introduction of the candidate's professional background.
                    Core Skills and Achievements: Highlight the candidate’s experience in key areas relevant to the role. Provide not more than 3 measurable accomplishments or skills directly addressing the job description's priorities. Use a numbered bullet format for easy readability. Keep sentences short and avoid overgeneralizations or unrelated skills.
                    Fit for the Role: Emphasize how the candidate’s expertise uniquely positions them to solve the company’s challenges. If applicable, address unconventional background fit in a positive light. Start with 'I am experienced in `the number of` key areas relevant to this role, These are:', list it out in number bullet point format, separate each line with new line.
                    Conclusion: End with an enthusiastic statement about contributing to the company and a polite call to action for next steps.
                    
                    Tone:
                    Keep the tone professional yet conversational.
                    Use simple, clear English to ensure ease of understanding.
                    Avoid repetition, overused phrases, or unsupported claims.
                    
                    Format:
                    Each paragraph should be under 50 words.
                    Avoid repeating too much from the resume; focus on value to the company.
                    Deliver the response in plain text paragraphs, structured for clarity.
                    
                    Inputs:
                    Job Title: {job_title}
                    Job Description: {job_description}
                    Resume: {resume_text}
                    
                    Output:
                    Write the introduction as a short, engaging, and conversational response in plain text format, ensuring each sentence demonstrates value and relevance to the role.
                    """
                    
                if model_provider == "Gemini":
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(model_name)
                
                    response = model.generate_content(
                        prompt.format(job_title=job_title, job_description=job_description, resume_text=resume_text)
                    )

                    introduction_text = response.text
                    st.write(introduction_text)
                elif model_provider == "Groq":
                    from groq import Groq
                    client = Groq(api_key=api_key)
                    chat_completion = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {
                                "role": "user",
                                "content": prompt.format(job_title=job_title, job_description=job_description, resume_text=resume_text),
                            }
                        ],
                    )
                    introduction_text = chat_completion.choices[0].message.content
                    st.write(introduction_text)
                # Generate speech
                audio_file = generate_speech(introduction_text, "tellmeaboutyourself.wav")
                if audio_file:
                    # Play audio in Streamlit
                    st.audio(audio_file)
        else:
            st.warning("Please enter job title, job description, resume, API key and select a model.")
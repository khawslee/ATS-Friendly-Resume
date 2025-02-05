import streamlit as st
import google.generativeai as genai


def bullet_point_rephaser_page(api_key, model_name, model_provider, job_title, job_description):
    st.title("📄 ATS Bullet Point Rephaser")

    # Bullet point input
    bullet_point = st.text_area("Paste the bullet point here")
    
    if st.button("Find keywords"):
        if job_description and model_name:
            with st.spinner("Analyzing..."):
                if model_provider == "Gemini":
                    # Set your Google Generative AI API key
                    genai.configure(api_key=api_key)
                    # Send to Google Generative AI for matching score
                    model = genai.GenerativeModel(model_name)
                elif model_provider == "Groq":
                    from groq import Groq
                    client = Groq(api_key=api_key)
                    chat_completion_keywords = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": f"You are a highly skilled ATS (Applicant Tracking System) scanner with expert-level knowledge of ATS standards and functionality. Your task is to extract and list only the most relevant keywords from the provided job description. Ensure that each keyword aligns precisely with the job title and its core requirements. Be concise, accurate, and provide the keyword per line end separate by comma without any additional explanations or irrelevant terms. Do not generate or fabricate any content beyond what is present in the job description.\n\nJob title:{job_title}\n\nJob description:{job_description}"
                            }
                        ],
                        model=model_name,
                    )
                    st.write("Keywords:\n", chat_completion_keywords.choices[0].message.content)
                    chat_completion_rephrase = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": f"Please rephrase the following bullet point using the suggested keywords and incorporate quantifiable achievements and improvements, following the Google recruiter XYZ formula. Ensure the bullet points remain precise, concise, and optimized for ATS screening. Focus exclusively on bullet points without adding any new or fabricated information, give each suggested bullet point response below 40 words.\n\nBullet point:\n{bullet_point}\n\nSuggestions:\n{chat_completion_keywords.choices[0].message.content}"
                            }
                        ],
                        model=model_name,
                    )
                    st.write("\nRephrased Bullet Point:\n", chat_completion_rephrase.choices[0].message.content)
                    return
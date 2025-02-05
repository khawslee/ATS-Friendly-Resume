import streamlit as st
import google.generativeai as genai

def core_competencies_extractor_page(api_key, model_name, model_provider, job_description):
    st.title("📄 Core competencies extractor")
    
    if st.button("Extract"):
        if job_description and model_name:
            with st.spinner("Analyzing..."):
                if model_provider == "Gemini":
                    # Set your Google Generative AI API key
                    genai.configure(api_key=api_key)
                    # Send to Google Generative AI for matching score
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(
                        f"please give me 6 important core competencies from Job Description:\n{job_description}\nPlease explain the core competencies. and then please provide the core competencies separate by |"
                    )
                    st.write("Core competencies:\n\n", response.text)
                elif model_provider == "Groq":
                    from groq import Groq
                    client = Groq(api_key=api_key)
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": f"please give me 6 important core competencies from Job Description:\n{job_description}\nPlease explain the core competencies. and then please provide the core competencies separate by |",
                            }
                        ],
                        model=model_name,
                    )
                    st.write("Core competencies:\n\n", chat_completion.choices[0].message.content)
                    return
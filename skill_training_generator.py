import streamlit as st
from duckduckgo_search import DDGS

def skill_training_generator_page(api_key, model_name, model_provider, job_title, job_description):
    """
    Generates a page that lists required skills and training resources for a given job title and description.
    """
    st.header("Skill and Training Generator")

    if st.button("Generate Training Resources"):
        if not job_title or not job_description:
            st.warning("Please enter both job title and job description.")
            return

        if model_provider == "Gemini":
            import google.generativeai as genai
            if not api_key:
                st.warning("Please enter your Google Generative AI API key.")
                return
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
        elif model_provider == "Groq":
            from groq import Groq
            if not api_key:
                st.warning("Please enter your Groq API key.")
                return
            client = Groq(api_key=api_key)
            model = client.chat.completions.create
        else:
            st.error("Invalid model provider selected.")
            return

        prompt_skills = f"""
        Based on the following job title and job description,
        identify the required skills for this role and
        suggest how a candidate can prepare for this job role.
        Job Title: {job_title}
        Job Description: {job_description}
        
        Format the output in the following sections:
        1. Required Skills: List the skills in a numbered list format.
        2. Job Role Preparation: Provide guidance on how a candidate can prepare for this job role.
        """

        if model_provider == "Gemini":
            response_skills = model.generate_content(prompt_skills)
            required_skills = response_skills.text
        elif model_provider == "Groq":
            response_skills = model(model=model_name, messages=[{"role": "user", "content": prompt_skills}])
            required_skills = response_skills.choices[0].message.content

        st.subheader("Required Skills")
        st.markdown(required_skills)

        st.subheader("Training Resources")
        search_term = f"training courses tutorials for {job_title} skills"
        search_results = DDGS().text(search_term, max_results=5) # Limit to 5 for brevity

        if search_results:
            st.markdown("Here are some training resources found on the internet:")
            for i, result in enumerate(search_results):
                st.markdown(f"{i+1}. [{result['title']}]({result['href']})")
        else:
            st.warning("No training resources found using DuckDuckGo Search.")

import streamlit as st
import google.generativeai as genai
import re
import time
from utils import extract_text_from_pdf

def ats_friendly_resume_generator_page(api_key, model_name, model_provider, uploaded_file, job_description):
    st.title("📝 ATS Friendly Resume Generator")
    
    # Create two columns
    col1, col2 = st.columns(2)

    # Matching score input in the first column
    with col1:
        matching_score_input = st.number_input("Enter Matching Score", step=1, format="%d", value=90)  # Set default value to 90

    # Iteration count input in the second column
    with col2:
        iteration_count_input = st.number_input("Enter Iteration Count", step=1, format="%d", value=3)


    # Process button
    if st.button("Generate Optimized Resume"):
        if uploaded_file is not None and job_description and api_key and model_name:
            with st.spinner("Analyzing..."):
                # Extract text from PDF
                original_resume_text = extract_text_from_pdf(uploaded_file)
                resume_text = original_resume_text
                best_resume_text = original_resume_text  # Initialize best resume text
                best_matching_score = 0  # Initialize best matching score

                # Initialize iteration count and matching score
                iteration_count = 0
                matching_score = 0
                
                if model_provider == "Gemini":
                    # Set your Google Generative AI API key
                    genai.configure(api_key=api_key)
                    # Send to Google Generative AI for matching score
                    model = genai.GenerativeModel(model_name)
                elif model_provider == "Groq":
                    from groq import Groq
                    client = Groq(api_key=api_key)
                    
                

                suggestions = ""
                # Iterate until matching score reaches 85 or maximum iterations reached
                while matching_score < matching_score_input and iteration_count < iteration_count_input:
                    if model_provider == "Gemini":
                        response = model.generate_content(
                            f"You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of ATS functionality, your task is to evaluate the resume against the provided job description. Do not explain each steps, remove the thinking part and do not explain. Provide a Matching Score: in this format 'Matching Score:'\n\nResume:\n{resume_text}\n\nJob Description:\n{job_description}"
                        )
                    elif model_provider == "Groq":
                        chat_completion_matching_score = client.chat.completions.create(
                            messages=[
                                {"role": "user", "content": f"You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of ATS functionality, your task is to evaluate the resume against the provided job description. Do not explain each steps, remove the thinking part and do not explain. Provide a Matching Score: in this format 'Matching Score:'\n\nResume:\n{resume_text}\n\nJob Description:\n{job_description}"}
                            ],
                            model=model_name
                        )
                        response_text = chat_completion_matching_score.choices[0].message.content
                    time.sleep(5)

                    # Process response and extract matching score
                    if model_provider == "Gemini":
                        response_text = response.text
                    match = re.search(r"Matching Score:\s*([\d.]+)", response_text)  # Improved regex
                    if match:
                        matching_score = float(match.group(1))
                        st.write(f"Iteration {iteration_count + 1}: Matching Score: {matching_score}")
                        if matching_score > best_matching_score:
                            best_matching_score = matching_score
                            best_resume_text = resume_text  # Update best resume text
                            if matching_score >= matching_score_input:
                                break
                    else:
                        st.write("Matching score not found in response.")

                    # Send to Google Generative AI for suggestions
                    if model_provider == "Gemini":
                        response_suggesstions = model.generate_content(
                            f"Analyze the following resume and job description and recommend how to add the missing keywords and improve the resume and also provide a list of specific suggestions for improvement to the resume in the context of ATS standards, the suggestions should be one per line, without any explanations. Do not explain each steps, remove the thinking part and do not explain. please strictly follow ATS standards so that further rephasing will be accurate:\n\n"
                            f"Resume:\n{resume_text}\n\n"
                            f"Job Description:\n{job_description}\n\n"
                            "Suggestions:"
                        )
                        response_text = response_suggesstions.text
                    elif model_provider == "Groq":
                        chat_completion_suggestions = client.chat.completions.create(
                            messages=[
                                {"role": "user", "content": f"Analyze the following resume and job description and recommend how to add the missing keywords and improve the resume and also provide a list of specific suggestions for improvement to the resume in the context of ATS standards, the suggestions should be one per line, without any explanations. Do not explain each steps, remove the thinking part and do not explain. please strictly follow ATS standards so that further rephasing will be accurate:\n\nResume:\n{resume_text}\n\nJob Description:\n{job_description}\n\nSuggestions:"}
                            ],
                            model=model_name
                        )
                        response_text = chat_completion_suggestions.choices[0].message.content
                    time.sleep(5)

                    # Process response and extract suggestions
                    suggestions = re.findall(r"^(.*?)\n", response_text, re.MULTILINE)  # Modified regex

                    # Update resume text based on suggestions using genai
                    if suggestions:
                        if model_provider == "Gemini":
                            new_prompt = f"Please rephrase the following resume and suggestions according to ATS standards, add relevent keywords, including quantifiable measures and improvements. where possible, also maintain precise and concise points which will pass ATS screening. Do not explain each steps, remove the thinking part and do not explain.\n\nResume:\n{resume_text}\n\nSuggestions:\n{'\n'.join(suggestions)}\n\n"
                            response_newresume = model.generate_content(new_prompt)
                            resume_text = response_newresume.text
                        elif model_provider == "Groq":
                            chat_completion_rephrase_resume = client.chat.completions.create(
                                messages=[
                                    {"role": "user", "content": f"Please rephrase the following resume and suggestions according to ATS standards, add relevent keywords, including quantifiable measures and improvements. where possible, also maintain precise and concise points which will pass ATS screening. Do not explain each steps, remove the thinking part and do not explain.\n\nResume:\n{resume_text}\n\nSuggestions:\n{'\n'.join(suggestions)}\n\n"}
                                ],
                                model=model_name
                            )
                            resume_text = chat_completion_rephrase_resume.choices[0].message.content

                    # Increment iteration count
                    iteration_count += 1

                # Print each suggestion individually
                if suggestions:
                    st.write("Final Suggestions for Improvement:")
                    for suggestion in suggestions:
                        st.write(f"- {suggestion.strip()}")

                # Display final resume
                st.write("Final Improved Resume:")
                st.write(best_resume_text)

        else:
            st.warning("Please upload a resume and paste a job description and enter your API key and select a model.")
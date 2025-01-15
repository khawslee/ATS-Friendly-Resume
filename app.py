import pyttsx3 # Import the pyttsx3 library for text-to-speech

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

import streamlit as st # Import the Streamlit library for creating web apps
import PyPDF2 # Import the PyPDF2 library for working with PDF files
import google.generativeai as genai # Import the Google Generative AI library
import re # Import the regular expression library
import time # Import the time library

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    if pdf_file is None:
        return ""
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    # Initialize an empty string to store the text
    text = ""
    # Loop through each page in the PDF
    for page in pdf_reader.pages:
        # Extract the text from the page and append it to the text string
        text += page.extract_text()
    # Return the extracted text
    return text

# Make Streamlit page wide
st.set_page_config(page_title="ATS Resume Evaluation System", layout="wide")

# Create two columns for API key and model selection
col1, col2 = st.columns(2)

# API Key Input (Password Field) in the first column
with col1:
    api_key = st.text_input("Enter your Google Generative AI API key", type="password")

# Model selection dropdown in the second column
with col2:
    if api_key:
        genai.configure(api_key=api_key)
        model_list = [model.name for model in genai.list_models() if 'gemini' in model.name]
        model_name = st.selectbox("Select Gemini Model", model_list)
    else:
        model_name = None
        st.warning("Please enter your API key to select a model.")


# Job title input
job_title = st.text_input("Paste the job title here")

# Job description input
job_description = st.text_area("Paste the job description here")

# File uploader
uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Rephase to Google XYZ", "Core competencies extractor", "Bullet Point Rephaser", "ATS Friendly Resume Generator", "Generate Cover Letter", "Introduction Generator", "Top Interview Questions", "Common Interview Questions"])

if page == "Rephase to Google XYZ":
    st.title("📄 Rephase to Google Recruiter XYZ formula")
    
    # Bullet point input
    bullet_point = st.text_area("Paste the bullet point here")
    
    if st.button("Rephase"):
        if bullet_point and model_name:
            with st.spinner("Analyzing..."):
                # Set your Google Generative AI API key
                genai.configure(api_key=api_key)
                # Send to Google Generative AI for matching score
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    f"Please rephrase the following bullet point, incorporate quantifiable achievements and improvements, following the Google recruiter XYZ formula. Give each suggested bullet point response below 40 words. Ensure the bullet points optimized for ATS screening.Below is my bullet point to extract relevent information:\n{bullet_point}"
                )
                st.write("Rephrased Bullet Point:\n", response.text)
                
if page == "Core competencies extractor":
    st.title("📄 Core competencies extractor")
    
    if st.button("Extract"):
        if job_description and model_name:
            with st.spinner("Analyzing..."):
                # Set your Google Generative AI API key
                genai.configure(api_key=api_key)
                # Send to Google Generative AI for matching score
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    f"please give me 6 important core competencies from Job Description:\n{job_description}\nPlease explain the core competencies. and then please provide the core competencies separate by |"
                )
                st.write("Core competencies:\n\n", response.text)

if page == "Bullet Point Rephaser":
    st.title("📄 ATS Bullet Point Rephaser")

    # Bullet point input
    bullet_point = st.text_area("Paste the bullet point here")
    
    if st.button("Find keywords"):
        if job_description and model_name:
            with st.spinner("Analyzing..."):
                # Set your Google Generative AI API key
                genai.configure(api_key=api_key)
                # Send to Google Generative AI for matching score
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    f"You are a highly skilled ATS (Applicant Tracking System) scanner with expert-level knowledge of ATS standards and functionality. Your task is to extract and list only the most relevant keywords from the provided job description. Ensure that each keyword aligns precisely with the job title and its core requirements. Be concise, accurate, and provide the keyword per line end separate by comma without any additional explanations or irrelevant terms. Do not generate or fabricate any content beyond what is present in the job description.\n\nJob title:{job_title}\n\nJob description:{job_description}"
                )
                #st.write(response.text)
                
                response_rephase = model.generate_content(
                    f"Please rephrase the following bullet point using the suggested keywords and incorporate quantifiable achievements and improvements, following the Google recruiter XYZ formula. Ensure the bullet points remain precise, concise, and optimized for ATS screening. Focus exclusively on bullet points without adding any new or fabricated information, give each suggested bullet point response below 40 words.\n\nBullet point:\n{bullet_point}\n\nSuggestions:\n{response.text}"
                )
                st.write("Keywords:\n", response.text)
                st.write("\nRephrased Bullet Point:\n", response_rephase.text)

elif page == "ATS Friendly Resume Generator":
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
                # Set your Google Generative AI API key
                genai.configure(api_key=api_key)

                # Extract text from PDF
                original_resume_text = extract_text_from_pdf(uploaded_file)
                resume_text = original_resume_text
                best_resume_text = original_resume_text  # Initialize best resume text
                best_matching_score = 0  # Initialize best matching score

                # Initialize iteration count and matching score
                iteration_count = 0
                matching_score = 0
                
                # Send to Google Generative AI for matching score
                model = genai.GenerativeModel(model_name)

                suggestions = ""
                # Iterate until matching score reaches 85 or maximum iterations reached
                while matching_score < matching_score_input and iteration_count < iteration_count_input:
                    response = model.generate_content(
                        f"You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of ATS functionality, your task is to evaluate the resume against the provided job description. Provide a Matching Score: in this format 'Matching Score:'\n\nResume:\n{resume_text}\n\nJob Description:\n{job_description}"
                    )
                    time.sleep(5)

                    # Process response and extract matching score
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
                    response_suggesstions = model.generate_content(
                        f"Analyze the following resume and job description and recommend how to add the missing keywords and improve the resume and also provide a list of specific suggestions for improvement to the resume in the context of ATS standards, the suggestions should be one per line, without any explanations. please strictly follow ATS standards so that further rephasing will be accurate:\n\n"
                        f"Resume:\n{resume_text}\n\n"
                        f"Job Description:\n{job_description}\n\n"
                        "Suggestions:"
                    )
                    time.sleep(5)

                    # Process response and extract suggestions
                    response_text = response_suggesstions.text
                    suggestions = re.findall(r"^(.*?)\n", response_text, re.MULTILINE)  # Modified regex

                    # Update resume text based on suggestions using genai
                    if suggestions:
                        new_prompt = f"Please rephrase the following resume and suggestions according to ATS standards, add relevent keywords, including quantifiable measures and improvements. where possible, also maintain precise and concise points which will pass ATS screening\n\nResume:\n{resume_text}\n\nSuggestions:\n{'\n'.join(suggestions)}\n\n"
                        response_newresume = model.generate_content(new_prompt)
                        resume_text = response_newresume.text

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
    
elif page == "Generate Cover Letter":
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
					You are an expert career assistant specializing in crafting compelling cover letter. Perform the following tasks step-by-step:

					Step 1. Analyze and Summarize Challenges: Carefully read the provided job description and identify the biggest day-to-day challenge someone in the role would face. Write the summary in a concise and professional tone.
					Step 2. Create an Attention-Grabbing Hook: Based on the summarized challenge, write a captivating opening sentence or hook that highlights how a candidate with the right skills can overcome this challenge. Keep it as reference in the cover letter.

                    Guidelines:
                    The cover letter are separate in 3 parts,
                    1. Descript who you are. Write one sentence about who you are as a professional. Please refer to the Attention-Grabbing Hook in Step 2.
                    2. Descript how are you a fit for the role. Avoid saying big thing about how your organizational skills or resourcefulness is really going to make you the best person. Read the job description and pick up the major themes and biggest problems that will need to be solved, then use that section to write in the cover letter why you are uniquely fit to solve it. Tell a story or explain why are you are a fit despite an unconventional background, do not simply repeat the experience listed on the resume. Make it short and simple and easy to read.
                    3. Explain why you are interested in this particular company. This could be as short as one sentence. Reiterate interest, express excitement to contribute, and include a call to action for the next steps.
					
                    Please make sure each paragraph is within 50 words, easy to read, short and consise, do not repeat too much from the resume and the cover letter is about what I can bring value to the company. Please make each sentences spicy. Reduce unnecessary fluff.
                    
					Inputs:
                    Job Title: {job_title}
					Job Description: {job_description}.
					Resume: {resume_text}.
					
					Output:
					Provide the results for each step separately. Clearly label them as "Step 1: Challenge Summary," "Step 2: Hook," and "Step 3: Cover Letter.
                    """
                
                prompt2 = """
					You are an expert career assistant specializing in crafting compelling cover letter. Perform the following tasks step-by-step:

					- Analyze and Summarize Challenges: Carefully read the provided job description and identify the biggest day-to-day challenge someone in the role would face. Write the summary in a concise and professional tone.
					- Create an Attention-Grabbing Hook: Based on the summarized challenge, write a captivating opening sentence or hook that highlights how a candidate with the right skills can overcome this challenge.
					- Draft a Cover Letter: Using the hook from Step 2 as the opening paragraph, write a professional cover letter tailored to the job description.
                    
                    Guidelines:
                    - Align the cover letter with the specific job description, incorporating relevant keywords, essential skills, and qualifications from the provided resume.
                    - Demonstrate how the candidate's experience, accomplishments, and skills make them the ideal fit for the role.
                    - Keep the tone professional and engaging, expressing enthusiasm for the role and the company.
                    - The cover letter must be concise (approximately one page) with a clear structure:
                    - Opening Paragraph: Using the hook from Step 2.
                    - Body Paragraph(s): Showcase only relevant skills and achievements with matric which with the company’s needs.
                    - Closing Paragraph: Reiterate interest, express excitement to contribute, and include a call to action for the next steps.
                    - Avoid repetition and ensure every sentence adds value, demonstrating expertise in crafting impactful cover letters.
                    Generate a final output that is ATS-friendly, polished, and tailored for maximum impact.
                    Keep each paragraph is within 50 words, easy to read, short and consise, do not repeat too much from the resume and the cover letter is about what I can bring value to the company.
					
					Inputs:
                    Job Title: {job_title}
					Job Description: {job_description}.
					Resume: {resume_text}.
					
					Output:
					Provide the results for each step separately. Clearly label them as "Step 1: Challenge Summary," "Step 2: Hook," and "Step 3: Cover Letter.
                    """
                
                prompt = prompt1 if prompt_option == "Short" else prompt2
                response = model.generate_content(
                    prompt.format(job_title=job_title, job_description=job_description, resume_text=resume_text)
                )
                st.write("Cover letter:\n", response.text)
                
elif page == "Introduction Generator":
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
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[0].id)
                engine.save_to_file(introduction_text, 'introduction.mp3')
                engine.runAndWait()
                engine.stop()

                # Play audio in Streamlit
                st.audio('introduction.mp3')
        else:
            st.warning("Please enter job title, job description, resume, API key and select a model.")
            
elif page == "Top Interview Questions":
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
            
elif page == "Common Interview Questions":
    st.title("Common Interview Questions")
    
    #List of questions
    listofQuestion = ["What makes you unique?", "Tell me about yourself and your qualifications.", "Why do you want to work at this company?", "What interests you about this role?", "What motivates you?", "What are your greatest strengths?", "What are your greatest weaknesses?", "What are your goals for the future?", "Where do you think you'll be in five years?", "What did you like most about your last position?", "What did you like least about your last position?", "Can you tell me about a difficult work situation and how you overcame it?", "How do you respond to stress or change?", "How do you handle conflict at work?", "What is your greatest accomplishment?", "How do you define success?", "How do your skills align with this role?", "Why should we hire you?", "Why are you leaving your current job?", "What is your salary range expectation?", "Do you have any questions?", "What are you passionate about?", "What is your teaching philosophy?", "What does customer service mean to you?", "Tell me about your work experience.", "How do you work under pressure?", "What is your dream job?", "What can you bring to the company?"]
    
    if st.button("Generate Questions and Answers"):
        if job_description and model_name and api_key and uploaded_file:
            with st.spinner("Generating..."):
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name)
                resume_text = extract_text_from_pdf(uploaded_file)
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

st.sidebar.markdown("---")
st.sidebar.markdown("© 2024 khawslee. All rights reserved.")

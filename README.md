[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

# ATS-Friendly-Resume

This application is designed to help job seekers create resumes that are optimized for Applicant Tracking Systems (ATS). It leverages Google's Generative AI to provide several tools for improving your resume and cover letter.

## Features

*   **Rephrase to Google Recruiter XYZ formula:** \
Rephrases bullet points to incorporate quantifiable achievements and improvements, following the Google recruiter XYZ formula.

*   **Core competencies extractor:** \
Extracts core competencies from a job description.

*   **ATS Bullet Point Rephaser:** \
Rephrases bullet points using keywords extracted from the job description, optimized for ATS screening.

*   **ATS Friendly Resume Generator:** \
Generates an optimized resume by analyzing the original resume and job description, and iteratively improving it based on a matching score.

*   **ATS Friendly Cover Letter Generator:** \
Generates a cover letter tailored to the job description, using the resume as input.

*   **Introduction Generator:** \
Generates a self-introduction based on the job title, job description, and resume.

*   **Top Interview Questions:** \
Generates the top 5 most relevant interview questions based on the job description and resume.

*   **Common Interview Questions:** \
Generates answers to common interview questions based on the job description and resume.

## How to Use

1.  **API Key:** Enter your Google Generative AI API key.
2.  **Job Title:** Paste the job title.
3.  **Job Description:** Paste the job description.
4.  **Resume Upload:** Upload your resume in PDF format.
5.  **Navigation:** Use the sidebar to navigate between the different tools.
6.  **Use the tools:** Each tool has its own specific inputs and outputs. Follow the instructions on the screen to use each tool.

## Requirements

*   Python 3.11+
*   Streamlit
*   PyPDF2
*   google-generativeai
*   pyttsx3
*   An active Google Generative AI API key

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/khawslee/ATS-Friendly-Resume.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd ATS-Friendly-Resume
    ```
3.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

## Contributing

Feel free to contribute to this project by submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

[contributors-shield]: https://img.shields.io/github/contributors/khawslee/ATS-Friendly-Resume.svg?style=for-the-badge
[contributors-url]: https://github.com/khawslee/ATS-Friendly-Resume/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/khawslee/ATS-Friendly-Resume.svg?style=for-the-badge
[forks-url]: https://github.com/khawslee/ATS-Friendly-Resume/network/members
[stars-shield]: https://img.shields.io/github/stars/khawslee/ATS-Friendly-Resume.svg?style=for-the-badge
[stars-url]: https://github.com/khawslee/ATS-Friendly-Resume/stargazers
[issues-shield]: https://img.shields.io/github/issues/khawslee/ATS-Friendly-Resume.svg?style=for-the-badge
[issues-url]: https://github.com/khawslee/ATS-Friendly-Resume/issues
[license-shield]: https://img.shields.io/github/license/khawslee/ATS-Friendly-Resume.svg?style=for-the-badge
[license-url]: https://github.com/khawslee/ATS-Friendly-Resume/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/khawslee

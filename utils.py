import PyPDF2
import pyttsx3

def generate_speech(text, filename, lang='en'):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 180) 
        engine.save_to_file(text, filename)
        engine.runAndWait()
        return filename
    except Exception as e:
        print(f"Error generating speech: {e}")
        return None

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
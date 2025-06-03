# Resume Analyzer

A Streamlit application that analyzes resumes against job descriptions using Groq's AI capabilities. The application provides detailed feedback on resume strengths, weaknesses, and suggestions for improvement.

## Features

- Upload resumes in PDF or DOCX format
- Analyze resume against any job description
- Get detailed feedback including:
  - Strengths that match the job requirements
  - Areas for improvement
  - Specific suggestions to increase chances of selection
- Modern, user-friendly interface
- Support for both PDF and DOCX resume formats

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
   You can get a Groq API key by signing up at https://console.groq.com/

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run ui.py
   ```
2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)
3. Upload your resume (PDF or DOCX format)
4. Paste the job description you want to analyze against
5. Click "Analyze Resume" to get detailed feedback

## Requirements

- Python 3.8 or higher
- Streamlit
- Groq API key
- Other dependencies listed in requirements.txt

## Note

Make sure to keep your Groq API key secure and never commit it to version control. The `.env` file is already included in `.gitignore` to prevent accidental exposure of your API key.
import streamlit as st
import os
from main import analyze_resume
import tempfile
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("Resume Analyzer 📄")
st.markdown("Upload your resume and job description to get personalized analysis and improvement suggestions.")

# File upload section
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=['pdf', 'docx'])

# Job description input
job_description = st.text_area(
    "Paste the job description here",
    height=200,
    placeholder="Enter the job description to analyze your resume against..."
)

# Submit button
if st.button("Analyze Resume", type="primary"):
    if uploaded_file is None:
        st.error("Please upload a resume file.")
    elif not job_description.strip():
        st.error("Please enter a job description.")
    else:
        with st.spinner("Analyzing your resume..."):
            try:
                # Save the uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name

                # Extract text based on file type
                if uploaded_file.name.endswith('.pdf'):
                    with open(tmp_file_path, 'rb') as file:
                        pdf_reader = PdfReader(file)
                        resume_text = ""
                        for page in pdf_reader.pages:
                            resume_text += page.extract_text()
                else:  # docx
                    doc = Document(tmp_file_path)
                    resume_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])

                # Clean up the temporary file
                os.unlink(tmp_file_path)

                # Get analysis from backend
                analysis = analyze_resume(resume_text, job_description)

                # Display results
                st.markdown("## Analysis Results")
                
                # Display overall assessment
                st.markdown("### 📊 Overall Assessment")
                st.markdown(analysis.get('assessment', 'Assessment not available'))
                
                # Display strengths
                st.markdown("### 💪 Strengths")
                st.markdown(analysis['strengths'])
                
                # Display weaknesses
                st.markdown("### ⚠️ Areas for Improvement")
                st.markdown(analysis['weaknesses'])
                
                # Display suggestions
                st.markdown("### 💡 Suggestions for Improvement")
                st.markdown(analysis['suggestions'])

            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")

# Add some helpful information
with st.expander("ℹ️ How to use this tool"):
    st.markdown("""
    1. Upload your resume in PDF or DOCX format
    2. Paste the job description you want to analyze against
    3. Click 'Analyze Resume' to get detailed feedback
    4. Review the overall assessment, strengths, weaknesses, and suggestions for improvement
    
    The analysis will help you:
    - Get an overall assessment of your fit for the position
    - Identify your key strengths for the position
    - Find areas where your resume could be improved
    - Get specific suggestions to increase your chances of selection
    """) 
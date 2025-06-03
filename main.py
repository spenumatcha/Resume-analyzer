import os
from dotenv import load_dotenv
from groq import Groq
import json
import re

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_json_from_response(response_text):
    # Try to extract the first JSON object from the response using regex
    match = re.search(r'\{[\s\S]*\}', response_text)
    if match:
        return match.group(0)
    return response_text

def analyze_resume(resume_text: str, job_description: str) -> dict:
    """
    Analyze the resume against the job description using Groq API.
    
    Args:
        resume_text (str): The text content of the resume
        job_description (str): The job description to analyze against
        
    Returns:
        dict: Analysis results containing strengths, weaknesses, and suggestions
    """
    
    prompt = f"""You are an expert resume analyzer and career coach. Analyze the following resume against the given job description.
    Provide a detailed analysis in the following JSON format:
    {{
        "strengths": "List the candidate's key strengths that match the job requirements. Format as bullet points.",
        "weaknesses": "List areas where the resume could be improved to better match the job requirements. Format as bullet points.",
        "suggestions": "Provide specific, actionable suggestions to improve the resume and increase chances of selection. Format as bullet points.",
        "assessment": "Provide a brief overall assessment of the candidate's fit for the position (2-3 sentences)."
        "Match Percentage": percentage match to the Job description
    }}

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Focus on:
    1. Skills and qualifications match
    2. Experience relevance
    3. Achievements and impact
    4. Overall presentation and formatting
    5. Specific improvements that would make the candidate more competitive
    6. Match percentage 

    Important:
    - Your response must be a valid JSON object with exactly these keys: strengths, weaknesses, suggestions, and assessment.
    - Do NOT include any markdown, code block, XML, or HTML tags. Output only the raw JSON object, nothing else.
    - Do NOT include any explanations or extra text before or after the JSON.
    - If you cannot analyze, return a JSON object with empty strings for all fields.
    """

    try:
        # Call Groq API
        completion = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",  # Using DeepSeek Llama 70B model
            messages=[
                {"role": "system", "content": "You are an expert resume analyzer and career coach. You must respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,  # Lower temperature for more consistent JSON output
            max_tokens=2000,
            top_p=1,
            stream=False
        )

        # Extract and parse the response
        response_text = completion.choices[0].message.content.strip()
        
        # Remove any markdown code block indicators if present
        response_text = response_text.replace('```json', '').replace('```', '').strip()
        
        # Try to extract JSON from the response
        json_str = extract_json_from_response(response_text)
        
        try:
            analysis = json.loads(json_str)
            # Validate the required keys are present
            required_keys = ['strengths', 'weaknesses', 'suggestions', 'assessment']
            if not all(key in analysis for key in required_keys):
                missing_keys = [key for key in required_keys if key not in analysis]
                raise ValueError(f"Missing required keys in analysis: {missing_keys}")
            # Ensure all values are strings
            for key in required_keys:
                if not isinstance(analysis[key], str):
                    analysis[key] = str(analysis[key])
            return analysis
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {str(e)}")
            print(f"Raw response: {response_text}")
            return {
                "strengths": "Error: Could not parse the analysis results. Please try again.",
                "weaknesses": "The system encountered an error while processing your resume.",
                "suggestions": "Please ensure your resume and job description are properly formatted and try again.",
                "assessment": "Unable to complete the analysis at this time."
            }

    except Exception as e:
        print(f"API Error: {str(e)}")
        return {
            "strengths": f"Error during analysis: {str(e)}",
            "weaknesses": "The system encountered an error while processing your request.",
            "suggestions": "Please try again or contact support if the issue persists.",
            "assessment": "Analysis could not be completed due to a system error."
        }

if __name__ == "__main__":
    # This block is for testing the analysis function directly
    test_resume = """
    John Doe
    Software Engineer
    
    Experience:
    - Senior Developer at Tech Corp (2020-Present)
    - Junior Developer at Startup Inc (2018-2020)
    
    Skills:
    - Python, JavaScript, React
    - AWS, Docker
    - Agile methodologies
    """
    
    test_job = """
    Senior Software Engineer
    
    Requirements:
    - 5+ years of experience in software development
    - Strong knowledge of Python and JavaScript
    - Experience with cloud platforms (AWS preferred)
    - Experience with containerization
    - Strong problem-solving skills
    """
    
    try:
        result = analyze_resume(test_resume, test_job)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}") 
from groq import Groq
import os
from dotenv import load_dotenv

def test_groq_api():
    print("Testing Groq API connection...")
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env file")
        return
    
    print(f"API Key found: {api_key[:8]}...{api_key[-4:]}")  # Show only first 8 and last 4 characters
    
    # Initialize client
    try:
        client = Groq(api_key=api_key)
        print("Groq client initialized successfully")
        
        # Test API call
        print("\nTesting API call with deepseek-r1-distill-llama-70b model...")
        completion = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[{"role": "user", "content": "Say hello in one word"}],
            max_tokens=10
        )
        
        print("\nAPI Response:")
        print(completion.choices[0].message.content)
        print("\nAPI test successful! Your Groq API key is working correctly.")
        
    except Exception as e:
        print(f"\nError during API test: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Verify your API key is correct")
        print("2. Check your internet connection")
        print("3. Ensure you have sufficient credits in your Groq account")
        print("4. Visit https://console.groq.com to check your API key status")

if __name__ == "__main__":
    test_groq_api() 
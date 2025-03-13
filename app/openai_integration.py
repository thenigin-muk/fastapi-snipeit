# app/openai_integration.py
import openai
from app.config import OPENAI_API_KEY

# Initialize OpenAI client
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

def query_openai(assets_summary, user_message):
    prompt = f"""
    You're an IT asset assistant. Use this data:
    
    {assets_summary}

    User's Question: {user_message}
    """

    try:
        openai_response = openai_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return openai_response.choices[0].message.content
    except Exception as e:
        return f"OpenAI Error: {str(e)}"

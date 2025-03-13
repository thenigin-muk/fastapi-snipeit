# app/config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SNIPE_IT_API_URL = "https://mukilteowa.snipe-it.io/api/v1"
SNIPE_IT_API_KEY = os.getenv("SNIPE_IT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AZURE_BOT_APP_ID = os.getenv("AZURE_BOT_APP_ID")
AZURE_BOT_APP_PASSWORD = os.getenv("AZURE_BOT_APP_PASSWORD")

if not all([SNIPE_IT_API_KEY, OPENAI_API_KEY, AZURE_BOT_APP_ID, AZURE_BOT_APP_PASSWORD]):
    raise ValueError("❌ Missing one or more required API keys in .env file.")

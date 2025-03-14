# app/config.py
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SNIPE_IT_API_URL = "https://mukilteowa.snipe-it.io/api/v1"
SNIPE_IT_API_KEY = os.getenv("SNIPE_IT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AZURE_BOT_APP_ID = os.getenv("AZURE_BOT_APP_ID")
AZURE_BOT_APP_PASSWORD = os.getenv("AZURE_BOT_APP_PASSWORD")

# Read debug setting from .env
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Create logs directory if it doesn't exist
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

# Configure logging based on DEBUG flag
if DEBUG:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "debug.log"),  # Log to project's logs directory
            logging.StreamHandler()  # Also output to console
        ]
    )
else:
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "app.log")  # Log to project's logs directory
        ]
    )

if not all([SNIPE_IT_API_KEY, OPENAI_API_KEY, AZURE_BOT_APP_ID, AZURE_BOT_APP_PASSWORD]):
    raise ValueError("❌ Missing one or more required API keys in .env file.")
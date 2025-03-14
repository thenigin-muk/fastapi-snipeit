# app/openai_integration.py
import openai
import logging
from .config import OPENAI_API_KEY, DEBUG

# Initialize OpenAI client
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Set up logging based on DEBUG flag
if DEBUG:
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
else:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.WARNING)

def query_openai(snipeit_summary, carrier_summary, categories_summary, user_message):
    logger = logging.getLogger(__name__)
    
    # Check if the summary contains the asset tag we're looking for
    if "00427" in snipeit_summary:
        logger.warning(f"Asset tag 00427 IS included in the OpenAI prompt")
    else:
        logger.warning(f"Asset tag 00427 is NOT included in the OpenAI prompt")
    
    # Log the lengths of the summaries if DEBUG is True
    if DEBUG:
        logger.info(f"snipeit_summary length: {len(snipeit_summary)}")
        logger.info(f"carrier_summary length: {len(carrier_summary)}")
        logger.info(f"categories_summary length: {len(categories_summary)}")
    
    prompt = f"""
    You are an IT asset assistant. You have access to the following data:

    Snipe-IT Data (Assets):
    {snipeit_summary}

    Mobile Carrier Data:
    {carrier_summary}

    Snipe-IT Categories:
    {categories_summary}

    The data is structured as follows:
    - Snipe-IT Data: Information about IT assets including name, tag, status, model, category, assigned to, location, and serial
    - Mobile Carrier Data: Information about mobile devices including device name, IMEI, SIM, phone number, carrier, and cost center
    - Snipe-IT Categories: Categories of assets including name, type, asset count, and item count

    Please answer the user's questions based on the data provided. Be flexible with spelling errors in the user's questions.
    If the information is partially available but not complete, provide what you can find rather than saying it's not available.
    Look for similar or related information if exact matches aren't found.

    User's Question: {user_message}
    """

    try:
        openai_response = openai_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return openai_response.choices[0].message.content
    except Exception as e:
        if DEBUG:
            logger.error(f"OpenAI Error: {str(e)}")
        return f"OpenAI Error: {str(e)}"

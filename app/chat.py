# app/chat.py
from fastapi import Request, HTTPException
import httpx
from typing import Tuple
import logging
from .openai_integration import query_openai
from .azure_auth import get_azure_auth_token
from .config import DEBUG

# Set up logging based on DEBUG flag
if DEBUG:
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler("/tmp/snipeit_debug.log"), 
                                logging.StreamHandler()])
    logger = logging.getLogger(__name__)
else:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.WARNING)

def process_user_query(user_message: str) -> Tuple[str, int]:
    # Example implementation: Extract category and limit from the user's query
    category = None
    limit = None

    if "smartphone" in user_message.lower():
        category = "Smartphone"
    if "first" in user_message.lower() and "assets" in user_message.lower():
        limit = 5

    return category, limit

def map_fieldsets_to_models(models, fieldsets):
    fieldset_map = {fieldset["id"]: fieldset["fields"] for fieldset in fieldsets}
    model_fieldset_map = {model["id"]: fieldset_map.get(model["fieldset_id"], []) for model in models}
    return model_fieldset_map

def summarize_data(data, model_fieldset_map, category=None, limit=None):
    if category:
        data = [item for item in data if item.get('category', {}).get('name') == category]
    if limit:
        data = data[:limit]
    summary = "\n".join([
        f"ID: {item.get('id', 'N/A')}, Name: {item.get('name', 'N/A')}, Tag: {item.get('asset_tag', 'N/A')}, "
        f"Model: {item.get('model', {}).get('name', 'N/A')}, Category: {item.get('category', {}).get('name', 'N/A')}, "
        f"Status: {item.get('status_label', {}).get('name', 'N/A')}, Assigned To: {item.get('assigned_to', {}).get('name', 'N/A')}, "
        f"Location: {item.get('location', {}).get('name', 'N/A')}, Last Checkout: {item.get('last_checkout', {}).get('formatted', 'N/A')}, "
        f"Custom Fields: {', '.join([f'{k}: {v.get('value', 'N/A')}' for k, v in item.get('custom_fields', {}).items() if k in model_fieldset_map.get(item.get('model', {}).get('id'), [])])}"
        for item in data
    ])
    return summary

async def process_chat(request: Request, carrier_data, snipeit_data, snipeit_categories, snipeit_fieldsets, snipeit_models):
    body = await request.json()

    if body.get("type") != "message":
        return {}

    user_message = body.get("text", "")
    service_url = body["serviceUrl"]
    conversation_id = body["conversation"]["id"]
    reply_to_id = body["id"]
    bot_id = body["recipient"]["id"]
    sender_id = body["from"]["id"]

    # Create asset summary with all assets, not limited
    asset_summary = "\n".join([
        f"• Name: {a.get('name', 'N/A')}, Tag: {a.get('asset_tag', 'N/A')}, "
        f"Status: {a.get('status', 'N/A')}, Model: {a.get('model', 'N/A')}, "
        f"Category: {a.get('category', 'N/A')}, "
        f"Assigned To: {a.get('assigned_to', 'N/A')}, "
        f"Location: {a.get('location', 'N/A')}, "
        f"Serial: {a.get('serial', 'N/A')}"
        for a in snipeit_data  # No limit on number of assets
    ])
    
    # Include all carrier data
    carrier_summary = "\n".join([
        f"• Device: {c.get('Device Name', 'N/A')}, IMEI: {c.get('IMEI', 'N/A')}, "
        f"SIM: {c.get('SIM', 'N/A')}, Phone Number: {c.get('Phone Number', 'N/A')}, "
        f"Carrier: {c.get('Carrier', 'N/A')}, Cost Center: {c.get('cost_center', 'N/A')}"
        for c in carrier_data  # No limit
    ])
    
    # Include all categories
    categories_summary = "\n".join([
        f"• Category: {c.get('name', 'N/A')}, Type: {c.get('category_type', 'N/A')}, "
        f"Asset Count: {c.get('assets_count', 'N/A')}, Item Count: {c.get('item_count', 'N/A')}"
        for c in snipeit_categories  # No limit
    ])

    # Log information only if DEBUG is True
    if DEBUG:
        logger.info(f"Total assets in snipeit_data: {len(snipeit_data)}")
        
        # Check for specific asset tag
        asset_427 = next((a for a in snipeit_data if a.get('asset_tag') == '00427'), None)
        if asset_427:
            logger.info(f"Found asset 00427: {asset_427}")
        else:
            logger.info("Asset tag 00427 not found in the dataset")
        
        # Display the first 10 asset tags for debugging
        first_10_tags = [a.get('asset_tag') for a in snipeit_data[:10]]
        logger.info(f"First 10 asset tags: {first_10_tags}")

    logger = logging.getLogger(__name__)
    
    # Search for asset tag 00427 in the data passed to the function
    asset_427 = next((asset for asset in snipeit_data if asset.get("asset_tag") == "00427"), None)
    if asset_427:
        logger.warning(f"Found asset 00427 in process_chat: {asset_427}")
    else:
        logger.warning(f"Asset tag 00427 NOT FOUND in process_chat")
        # Log the first 5 asset tags to see what's available
        first_5_tags = [asset.get("asset_tag") for asset in snipeit_data[:5]]
        logger.warning(f"First 5 asset tags in process_chat: {first_5_tags}")

    # Query OpenAI with all required arguments
    bot_response = query_openai(asset_summary, carrier_summary, categories_summary, user_message)

    # Get Azure Bot token
    token = await get_azure_auth_token()
    if not token:
        raise HTTPException(status_code=500, detail="Azure token authentication failed.")

    azure_headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    azure_response = {
        "type": "message",
        "from": {"id": bot_id},
        "recipient": {"id": sender_id},
        "conversation": {"id": conversation_id},
        "text": bot_response,
        "replyToId": reply_to_id,
    }

    async with httpx.AsyncClient() as http_client:
        await http_client.post(f"{service_url}/v3/conversations/{conversation_id}/activities/{reply_to_id}",
                               headers=azure_headers, json=azure_response)

    return {}

# app/snipeit_api.py
import requests
import json
import os
import tempfile
import logging
from fastapi import HTTPException
from .config import SNIPE_IT_API_URL, SNIPE_IT_API_KEY, DEBUG

# Use temp directory instead of cleaned_data
DATA_DIR = tempfile.gettempdir()

# Set up logging based on DEBUG flag
if DEBUG:
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
else:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.WARNING)

def get_snipeit_assets(debug=False):
    headers = {
        "Authorization": f"Bearer {SNIPE_IT_API_KEY}",
        "Accept": "application/json"
    }
    
    # Increase the limit to get more assets
    response = requests.get(f"{SNIPE_IT_API_URL}/hardware?limit=500", headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Snipe-IT API error: {response.status_code}")
    
    assets_json = response.json().get("rows", [])
    logger = logging.getLogger(__name__)
    logger.warning(f"Retrieved {len(assets_json)} assets from API")
    
    # Search for asset tag 00427
    asset_427 = next((asset for asset in assets_json if asset.get("asset_tag") == "00427"), None)
    if asset_427:
        logger.warning(f"Found asset 00427: {asset_427}")
    else:
        logger.warning(f"Asset tag 00427 NOT FOUND in API response")
        # Log the first 5 asset tags to see what's available
        first_5_tags = [asset.get("asset_tag") for asset in assets_json[:5]]
        logger.warning(f"First 5 asset tags: {first_5_tags}")

    formatted_assets = [
        {
            "id": asset.get("id", "UNKNOWN"),
            "name": asset.get("name", "UNKNOWN"),
            "asset_tag": asset.get("asset_tag", "UNKNOWN"),
            "serial": asset.get("serial", "UNKNOWN"),
            "model": asset.get("model", {}).get("name", "UNKNOWN"),
            "category": asset.get("category", {}).get("name", "UNKNOWN"),
            "status": asset.get("status_label", {}).get("status_meta", "UNKNOWN"),
            "assigned_to": (asset.get("assigned_to") or {}).get("name", "Unassigned"),
            "location": (asset.get("location") or {}).get("name", "UNKNOWN"),
            "last_checkout": (asset.get("last_checkout") or {}).get("formatted", "Never"),
            "custom_fields": asset.get("custom_fields", {})
        }
        for asset in assets_json
    ]

    if debug:
        logger.info(f"Retrieved {len(assets_json)} assets from API")
        
        # Log all asset tags to see if 00427 is among them
        all_asset_tags = [asset.get("asset_tag") for asset in assets_json]
        logger.info(f"All asset tags: {all_asset_tags}")
        
        # Check for specific asset tag
        asset_427 = next((a for a in assets_json if a.get("asset_tag") == "00427"), None)
        if asset_427:
            logger.info(f"Found asset 00427 in API response: {asset_427}")
        else:
            logger.info("Asset tag 00427 not found in API response")

    # Write to JSON for debugging
    if debug:
        with open(f"{DATA_DIR}/snipeit_assets.json", "w") as json_file:
            json.dump(formatted_assets, json_file, indent=4)
        print(f"✔ Debug JSON saved to {DATA_DIR}/snipeit_assets.json")

    return formatted_assets  # Store in-memory instead of always saving

def get_snipeit_categories(debug=False):
    headers = {
        "Authorization": f"Bearer {SNIPE_IT_API_KEY}",
        "Accept": "application/json"
    }
    response = requests.get(f"{SNIPE_IT_API_URL}/categories", headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Snipe-IT API error: {response.status_code}")

    categories_json = response.json().get("rows", [])
    formatted_categories = [
        {
            "id": category.get("id", "UNKNOWN"),
            "name": category.get("name", "UNKNOWN"),
            "category_type": category.get("category_type", "UNKNOWN"),
            "item_count": category.get("item_count", "UNKNOWN"),
            "assets_count": category.get("assets_count", "UNKNOWN"),
            "accessories_count": category.get("accessories_count", "UNKNOWN"),
            "consumables_count": category.get("consumables_count", "UNKNOWN"),
            "components_count": category.get("components_count", "UNKNOWN"),
            "licenses_count": category.get("licenses_count", "UNKNOWN"),
            "created_by": (category.get("created_by") or {}).get("name", "UNKNOWN")
        }
        for category in categories_json
    ]

    # Write to JSON for debugging
    if debug:
        with open(f"{DATA_DIR}/snipeit_categories.json", "w") as json_file:
            json.dump(formatted_categories, json_file, indent=4)
        print(f"✔ Debug JSON saved to {DATA_DIR}/snipeit_categories.json")

    return formatted_categories  # Store in-memory instead of always saving

def get_snipeit_fieldsets(debug=False):
    headers = {
        "Authorization": f"Bearer {SNIPE_IT_API_KEY}",
        "Accept": "application/json"
    }
    response = requests.get(f"{SNIPE_IT_API_URL}/fieldsets", headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Snipe-IT API error: {response.status_code}")

    fieldsets_json = response.json().get("rows", [])
    formatted_fieldsets = [
        {
            "id": fieldset.get("id", "UNKNOWN"),
            "name": fieldset.get("name", "UNKNOWN"),
            "fields": fieldset.get("fields", [])
        }
        for fieldset in fieldsets_json
    ]

    # Write to JSON for debugging
    if debug:
        with open(f"{DATA_DIR}/snipeit_fieldsets.json", "w") as json_file:
            json.dump(formatted_fieldsets, json_file, indent=4)
        print(f"✔ Debug JSON saved to {DATA_DIR}/snipeit_fieldsets.json")

    return formatted_fieldsets  # Store in-memory instead of always saving

def get_snipeit_models(debug=False):
    headers = {
        "Authorization": f"Bearer {SNIPE_IT_API_KEY}",
        "Accept": "application/json"
    }
    response = requests.get(f"{SNIPE_IT_API_URL}/models", headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Snipe-IT API error: {response.status_code}")

    models_json = response.json().get("rows", [])
    formatted_models = [
        {
            "id": model.get("id", "UNKNOWN"),
            "name": model.get("name", "UNKNOWN"),
            "fieldset_id": model.get("fieldset_id", "UNKNOWN")
        }
        for model in models_json
    ]

    # Write to JSON for debugging
    if debug:
        with open(f"{DATA_DIR}/snipeit_models.json", "w") as json_file:
            json.dump(formatted_models, json_file, indent=4)
        print(f"✔ Debug JSON saved to {DATA_DIR}/snipeit_models.json")

    return formatted_models  # Store in-memory instead of always saving

# app/main.py
from fastapi import FastAPI, Request, HTTPException
from typing import Tuple
from .normalize_carrier import normalize_carrier_data
from .snipeit_api import get_snipeit_assets, get_snipeit_categories, get_snipeit_fieldsets, get_snipeit_models
from .openai_integration import query_openai

app = FastAPI()

# Load and store carrier data + Snipe-IT data at startup
carrier_data = normalize_carrier_data(debug=True)
snipeit_data = get_snipeit_assets(debug=True)
snipeit_categories = get_snipeit_categories(debug=True)
snipeit_fieldsets = get_snipeit_fieldsets(debug=True)
snipeit_models = get_snipeit_models(debug=True)

@app.post("/chat")
async def chat_with_assets(request: Request):
    return await process_chat(request, carrier_data, snipeit_data, snipeit_categories, snipeit_fieldsets, snipeit_models)
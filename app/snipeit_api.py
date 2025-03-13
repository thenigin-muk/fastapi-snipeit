# app/snipeit_api.py
import requests
import json
import os
from fastapi import HTTPException
from config import SNIPE_IT_API_URL, SNIPE_IT_API_KEY

DATA_DIR = "cleaned_data"
os.makedirs(DATA_DIR, exist_ok=True)

def get_snipeit_assets(debug=False):
    headers = {
        "Authorization": f"Bearer {SNIPE_IT_API_KEY}",
        "Accept": "application/json"
    }
    response = requests.get(f"{SNIPE_IT_API_URL}/hardware?limit=50", headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Snipe-IT API error: {response.status_code}")

    assets_json = response.json().get("rows", [])
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

    # Write to JSON for debugging
    if debug:
        with open(f"{DATA_DIR}/snipeit_assets.json", "w") as json_file:
            json.dump(formatted_assets, json_file, indent=4)
        print(f"✔ Debug JSON saved to {DATA_DIR}/snipeit_assets.json")

    return formatted_assets  # Store in-memory instead of always saving

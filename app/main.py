# app/main.py
from fastapi import FastAPI, Request
from .chat import process_chat
from .normalize_carrier import normalize_carrier_data
from .snipeit_api import get_snipeit_assets, get_snipeit_categories, get_snipeit_fieldsets, get_snipeit_models

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

# app/main.py
from fastapi import FastAPI, Request
from app.chat import process_chat
from app.normalize_carrier import normalize_carrier_data
from app.snipeit_api import get_snipeit_assets

app = FastAPI()

# Load and store carrier data + Snipe-IT data at startup
carrier_data = normalize_carrier_data(debug=True)
snipeit_data = get_snipeit_assets(debug=True)

@app.post("/chat")
async def chat_with_assets(request: Request):
    return await process_chat(request, carrier_data, snipeit_data)

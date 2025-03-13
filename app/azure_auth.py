# app/azure_auth.py
import httpx
from app.config import AZURE_BOT_APP_ID, AZURE_BOT_APP_PASSWORD

async def get_azure_auth_token():
    auth_url = "https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token"
    data = {
        'grant_type': 'client_credentials',
        'client_id': AZURE_BOT_APP_ID,
        'client_secret': AZURE_BOT_APP_PASSWORD,
        'scope': 'https://api.botframework.com/.default'
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(auth_url, data=data)
        response.raise_for_status()
        return response.json().get('access_token')

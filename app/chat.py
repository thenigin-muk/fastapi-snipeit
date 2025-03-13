# app/chat.py
from fastapi import Request, HTTPException
import httpx
from app.snipeit_api import get_snipeit_assets
from app.openai_integration import query_openai
from app.azure_auth import get_azure_auth_token

async def process_chat(request: Request):
    body = await request.json()

    if body.get("type") != "message":
        return {}

    user_message = body.get("text", "")
    service_url = body["serviceUrl"]
    conversation_id = body["conversation"]["id"]
    reply_to_id = body["id"]
    bot_id = body["recipient"]["id"]
    sender_id = body["from"]["id"]

    # Fetch Snipe-IT assets
    assets = get_snipeit_assets()
    asset_summary = "\n".join([
        f"• {a['name']} (Tag: {a.get('asset_tag', 'N/A')}), Status: {a.get('status', 'N/A')}"
        for a in assets[:10]
    ])

    # Query OpenAI
    bot_response = query_openai(asset_summary, user_message)

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

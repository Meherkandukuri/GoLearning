from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from ..config import settings
from ..db import get_db
from .. import models
import httpx


router = APIRouter()


@router.get("/webhook")
async def verify_webhook(mode: str = "", token: str = "", challenge: str = ""):
    # Meta sends hub.mode, hub.verify_token, hub.challenge
    # FastAPI will map query params if names match
    if token != settings.whatsapp_verify_token:
        raise HTTPException(status_code=403, detail="Verification failed")
    return PlainTextResponse(challenge or "")


@router.post("/webhook")
async def receive_webhook(req: Request, db: Session = Depends(get_db)):
    payload = await req.json()
    # Minimal parsing – in production validate per WhatsApp schema
    # Echo a basic reply if we have access token configured
    try:
        entry = (payload.get("entry") or [{}])[0]
        changes = (entry.get("changes") or [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])
        if messages and settings.whatsapp_access_token and settings.whatsapp_phone_number_id:
            msg = messages[0]
            from_wa = msg.get("from")
            text = (msg.get("text") or {}).get("body", "")
            reply = build_auto_reply(text)
            await send_whatsapp_text(from_wa, reply)
    except Exception:
        # Avoid failing webhook delivery
        pass
    return {"received": True}


def build_auto_reply(text: str) -> str:
    text_lower = (text or "").strip().lower()
    if not text_lower:
        return "Welcome to Roots! Send 'menu' to see today's vegetables."
    if text_lower in {"hi", "hello"}:
        return "Hello from Roots 331! Send 'menu' for today's list or 'help'."
    if text_lower in {"menu", "list"}:
        return (
            "Roots Menu:\n- Tomato (kg)\n- Potato (kg)\n- Spinach (bunch)\nReply: 'order Tomato 1kg' to place an order."
        )
    if text_lower.startswith("order"):
        return "Got it! We will confirm your order shortly."
    return "Type 'menu' to see items or 'help' for assistance."


async def send_whatsapp_text(to_number: str, message: str):
    url = f"https://graph.facebook.com/v19.0/{settings.whatsapp_phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {settings.whatsapp_access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message},
    }
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(url, headers=headers, json=data)



# Roots - Backend

FastAPI backend for the Roots vegetable store with WhatsApp Cloud API integration.

## Quickstart

- Create venv and install deps:
  - python3 -m venv .venv
  - source .venv/bin/activate
  - pip install -r requirements.txt
- Environment variables (shell or .env):
  - DATABASE_URL=sqlite:///./roots.db
  - WHATSAPP_VERIFY_TOKEN=change-me
  - WHATSAPP_ACCESS_TOKEN=<from Meta>
  - WHATSAPP_PHONE_NUMBER_ID=<from Meta>
- Run server:
  - python run.py

Open http://localhost:8000/health

## Webhook setup

Expose your server (e.g., ngrok http 8000) and set webhook URL in Meta to:
https://<subdomain>.ngrok.io/whatsapp/webhook

## Endpoints

- /health
- /catalog (GET, POST, PUT, DELETE)
- /orders (GET, POST)
- /whatsapp/webhook (GET verify, POST receive)

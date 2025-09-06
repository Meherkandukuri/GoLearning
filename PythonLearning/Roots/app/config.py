import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Roots Store API"
    database_url: str = "sqlite:///./roots.db"

    # WhatsApp / Meta config
    whatsapp_verify_token: str = "change-me"
    whatsapp_access_token: str = ""
    whatsapp_phone_number_id: str = ""

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")


settings = Settings()



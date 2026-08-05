import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Creative Studio"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 50MB maximum upload limit to support high-fidelity raw 4K source images safely
    MAX_CONTENT_LENGTH: int = 50 * 1024 * 1024 
    
    # Allowed network origins ("*" allows universal cloud connections, perfect for mobile testing)
    ALLOWED_ORIGINS: list = ["*"]

settings = Settings()

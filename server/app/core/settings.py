import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    APP_NAME: str = "Crab"
    APP_DESCRIPTION: str = "Voice-based AI Assistant"
    APP_VERSION: str = "1.0.0"
    
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))  # Default port is 8000
    
    CORS_ORIGINS: List[str] = [
        
    ]
    
    # Model settings
    STT_MODEL: str = os.getenv("STT_MODEL", "openai/whisper-large-v3-turbo")
    TTS_MODEL: str = os.getenv("TTS_MODEL", "hexgrad/Kokoro-82M")
    INTENT_MODEL: str = os.getenv("INTENT_MODEL", "")  # TODO: Not configured
    
    # Wake word settings
    WAKE_WORD: str = os.getenv("WAKE_WORD", "hey crab")
    PORCUPINE_API_KEY: str = os.getenv("PORCUPINE_API_KEY", "")  # TODO: Not configured
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        

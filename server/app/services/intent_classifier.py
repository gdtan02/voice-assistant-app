from typing import Dict, Optional, Any, List

from app.core.settings import Settings

settings =  Settings()

class IntentClassifier:
    
    def __init__(self):
        pass
    
    async def classify(self, text: str, language: str = "en") -> Dict[str, Any]:
        return {
            "intent": "acceptOrder",  # Replace using ENUM
            "data": {}
        }
import io
import numpy as np
import soundfile as sf
from typing import Dict, Optional, Any, Union

from app.core.settings import Settings
from app.services.noise_reduction import NoiseReductionModel

class STTService:
    
    def __init__(self):
        pass
    
    async def transcribe(self, audio_data: bytes) -> Dict[str, Any]:
        return { 
                "text": "STT service is not implemented." ,
                "language": "en"
            }
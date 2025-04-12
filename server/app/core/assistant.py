import time
from typing import Dict, Any, Optional, List

from app.services.speech_to_text import STTService
from app.services.text_to_speech import TTSService
from app.services.intent_classifier import IntentClassifier
from app.services.wake_word import WakeWordDetector
from app.services.action_executor import ActionExecutor
from app.core.connection_manager import ConnectionManager
from app.core.settings import Settings

settings = Settings()

class Assistant:
    
    def __init__(self):
        
        # Get connection manager instance
        self.connection_manager = ConnectionManager()
        
        self.stt_service = STTService()
        self.tts_service = TTSService()
        self.intent_classifier = IntentClassifier()
        self.wake_word_detector = WakeWordDetector()
        self.action_executor = ActionExecutor()
        
    async def process_audio(self, audio_data: bytes, client_id: str) -> Optional[Dict[str, Any]]:
        
        try: 
            # Inactive session, wake up the assistant
            if not self.connection_manager.is_session_active(client_id):
                # Detect wake word
                wake_word_detected = True  # TODO: NotImplemented
                
                if wake_word_detected:
                    self.connection_manager.set_session_active(client_id=client_id, active=True)
                    
                response_text = "Hi, how can I help you today?"
                tts_response = await self.tts_service.synthesize(response_text)
                
                return {
                    "text": response_text,
                    "audio": tts_response.get("audio", ""),
                    "content_type": "audio/wav"
                }
            
            # Active session, process speech
            # 1. STT
            transcription = await self.stt_service.transcribe(audio_data)
            
            if not transcription or not transcription.get("text"):
                raise Exception(f"No speech detected for client {client_id}")
            
            text = transcription["text"]
            
            intent = await self.intent_classifier.classify(text, transcription.get("language", "en"))
            
            response = await self.action_executor.handle_intent(intent)
            
            if response["is_success"]:
                response_text = response["message"]
                tts_response = await self.tts_service.synthesize(response_text)
            
                return {
                    "text": response_text,
                    "audio": tts_response.get("audio", ""),
                    "content_type": "audio/wav"
                }  
                
            else:
                raise Exception(f"Failed to perform action for {client_id}")
                
        except Exception as e:
            print(f"Error: {e}")
            return {
                "text": "Sorry, I encountered a problem. Could you try again?",
                "audio": "",
                "content_type": "audio/wav"
            }
            
    async def process_event(self, event_type: str, event_data: Dict[str, Any], client_id: str) -> Optional[Dict[str, Any]]:
        
        try: 
            if event_type == "incoming_order":
                order_details = self._format_order_details(event_data)
                response_text = f"You have a new order request. {order_details} Would you like to accept or reject?"
                
                # setup a session wait and listen to client's response
                self.connection_manager.set_session_active(client_id=client_id, active=True)
                
                # Generate speech to inform user
                tts_response = await self.tts_service.synthesize(response_text)
                
                return {
                    "text": response_text,
                    "audio": tts_response,
                    "content_type": "audio/wav"
                }
                
            elif event_type == "navigation_alert":
                pass  # TODO: Implement other possible event triggers case
            
            # Unknown event type
            return None
        
        except Exception as e:
            return {
                "text": "Sorry, I encountered a problem and is not available to process upcoming events temporarily.",
                "audio": "",
                "content_type": "audio/wav"
            }
            
    
    def _format_order_details(self, order_data: Dict[str, Any]) -> str:
        pickup = order_data.get("pickup", "Unknown location")
        dropoff = order_data.get("dropoff", "Unknown destination")
        fare = order_data.get("fare", "Unknown amount")
        number_of_pax = order_data.get("number_of_pax", "Unknown amount")
        
        return f"Pickup {"a passenger" if number_of_pax == 1 else f"{number_of_pax} passengers"} from {pickup}, drop-off at {dropoff}. Fare is {fare}."
        
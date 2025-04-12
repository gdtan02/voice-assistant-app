import json
import base64
import asyncio
import uuid
from typing import Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.connection_manager import ConnectionManager
from app.core.assistant import Assistant
from app.core.settings import Settings

settings = Settings()

websocket_router = APIRouter()

connection_manager = ConnectionManager()

assistant = Assistant()

@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
   
    client_id = str(uuid.uuid4())
    
    await connection_manager.connect(websocket, client_id)
    # stop_audio_stream = False
    # audio_queue = asyncio.Queue()  # For incoming audio data
    
    try:
        print("WebSocket connection established: {client_id}")
        
        while True:
            message = await websocket.receive_text()
            message_type = message.get("type")
            
            try: 
                # TODO: Check if it supports audio-streaming
                # Audio input activation
                if message_type == "audio":
                    # Decode audio data
                    audio_data = base64.b64decode(message["data"])
                    response = await assistant.process_audio(audio_data, client_id)
                    
                    if response:
                        await connection_manager.send_message(
                            client_id,
                            {
                                "type": "speech",
                                "text": response.get("text"),
                                "audio": response.get("audio")
                            }
                        )
                
                # Event-trigger activation
                elif message_type == "event":
                    event_type = message.get("event_type")
                    event_data = message.get("data", {})
                    
                    connection_manager.set_session_active(client_id, True)
                    
                    response = await assistant.process_event(event_type, event_data, client_id)
                    
                    if response:
                        await connection_manager.send_message(client_id, response)
                        
            except json.JSONDecodeError:
                print("Invalid JSON object received")
            except Exception as e:
                print(f"Error processing message: {e}")
                    
    except WebSocketDisconnect:
        print("Websocket disconnected.")
    finally:
        await websocket.close()
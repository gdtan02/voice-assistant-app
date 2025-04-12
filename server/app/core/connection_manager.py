import time
from typing import Dict
from fastapi import WebSocket

class ConnectionManager:
    """
    Manages WebSocket connections and session states
    """
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.active_sessions: Dict[str, bool] = {}
        # self.session_timestamps: Dict[str, float] = {}   # TODO: To be implemented in future
        # self.session_timeout = 60
        
        
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.active_sessions[client_id] = False
        
        print(f"Client connected: {client_id}")
        
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        
        if client_id in self.active_sessions:
            del self.active_sessions[client_id]
            
        print(f"Client disconnected: {client_id}")
        
    async def send_message(self, client_id: str, message: Dict):
        """
        Send message to specific client
        """
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(message)
            print(f"Message send to client {client_id}: { message.get('type')}")
            print(f"Message content: {message}")  # Keep for DEBUG only
            
    
    def is_session_active(self, client_id: str) -> bool:
        return self.active_connections.get(client_id, False)
    
    def set_session_active(self, client_id: str, active: bool):
        self.active_sessions[client_id] = active
        print(f"Session for client {client_id} is set to { 'active' if active else 'inactive'}")
        
        

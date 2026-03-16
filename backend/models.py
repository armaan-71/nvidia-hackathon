from pydantic import BaseModel
from typing import Optional, Dict, List, Any
from datetime import datetime

class AgentResponse(BaseModel):
    message: str                # Natural language response for the chat UI
    active_agent: str          # e.g., "discovery", "analyzer", "scorer"
    session_id: str
    data: Optional[Dict[str, Any]] = None       # Structured payload (e.g., grant details, matches)
    suggested_actions: List[str] = [] # Buttons for UI
    timestamp: str = datetime.utcnow().isoformat()

class ChatRequest(BaseModel):
    message: str
    session_id: str

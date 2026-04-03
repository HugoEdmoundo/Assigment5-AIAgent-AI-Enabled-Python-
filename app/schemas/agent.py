from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class AgentRequest(BaseModel):
    query: str
    tools: List[str] = []
    session_id: Optional[str] = None

class AgentResponse(BaseModel):
    query: str
    tools_used: List[str]
    results: List[Dict[str, Any]]
    summary: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    response: str
    tools_used: List[str] = []
    session_id: str

class StreamChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

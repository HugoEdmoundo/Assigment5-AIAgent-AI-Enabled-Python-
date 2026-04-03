from pydantic import BaseModel
from typing import Dict, Any

class ToolRequest(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]

class ToolResponse(BaseModel):
    tool_name: str
    result: Any
    success: bool

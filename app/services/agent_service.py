from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.services.tool_service import ToolService
from app.services.llm_service import LLMService
from app.services.session_service import SessionService
from app.schemas.agent import AgentResponse

class AgentService:
    def __init__(self):
        self.tool_service = ToolService()
        self.llm_service = LLMService()
        self.session_service = SessionService()
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tool names"""
        return [tool["name"] for tool in self.tool_service.get_available_tools()]
    
    async def process_query(
        self, 
        query: str, 
        session_id: str = None,
        db: Session = None,
        requested_tools: List[str] = None
    ) -> AgentResponse:
        """Process user query using LLM and tools with session context"""
        tools_to_use = []
        results = []
        
        # Get conversation history if session exists
        conversation_history = []
        if session_id and db:
            conversation_history = self.session_service.get_conversation_history(
                db, session_id, limit=10
            )
        
        # Get available tools info
        available_tools = self.tool_service.get_available_tools()
        
        # Use LLM to understand the query
        llm_response = await self.llm_service.chat_with_tools(
            user_message=query,
            available_tools=available_tools,
            conversation_history=conversation_history
        )
        
        # Check if LLM wants to use a tool
        if llm_response["type"] == "tool_call":
            tool_name = llm_response["tool_name"]
            params = llm_response["parameters"]
            
            try:
                tool_result = self.tool_service.execute_tool(tool_name, params)
                tools_to_use.append(tool_name)
                results.append({
                    "tool": tool_name,
                    "parameters": params,
                    "result": tool_result
                })
                
                # Generate final response with tool result
                final_messages = conversation_history + [
                    {"role": "user", "content": query},
                    {"role": "assistant", "content": f"I used {tool_name} and got: {tool_result}. Let me explain..."},
                ]
                summary = await self.llm_service.chat(final_messages)
            except Exception as e:
                results.append({"tool": tool_name, "error": str(e)})
                summary = f"Error executing {tool_name}: {str(e)}"
        else:
            # Direct text response from LLM
            summary = llm_response["content"]
        
        # Save to session if provided
        if session_id and db:
            self.session_service.add_message(db, session_id, "user", query)
            self.session_service.add_message(db, session_id, "assistant", summary)
        
        return AgentResponse(
            query=query,
            tools_used=tools_to_use,
            results=results,
            summary=summary
        )

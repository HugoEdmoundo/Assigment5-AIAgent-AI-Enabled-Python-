from typing import Dict, Any, List, AsyncGenerator
from litellm import acompletion
from app.core.config import settings
import json

class LLMService:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = "openrouter/meta-llama/llama-3.1-8b-instruct:free"
    
    async def chat(self, messages: List[Dict[str, str]]) -> str:
        """Send chat request using LiteLLM"""
        if not self.api_key:
            return "Error: OpenRouter API key not configured"
        
        try:
            response = await acompletion(
                model=self.model,
                messages=messages,
                api_key=self.api_key,
                api_base="https://openrouter.ai/api/v1",
                timeout=30.0
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling LLM: {str(e)}"
    
    async def chat_stream(
        self, 
        messages: List[Dict[str, str]]
    ) -> AsyncGenerator[str, None]:
        """Stream chat response using LiteLLM"""
        if not self.api_key:
            yield "Error: OpenRouter API key not configured"
            return
        
        try:
            response = await acompletion(
                model=self.model,
                messages=messages,
                api_key=self.api_key,
                api_base="https://openrouter.ai/api/v1",
                stream=True,
                timeout=30.0
            )
            
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"Error: {str(e)}"
    
    async def chat_with_tools(
        self, 
        user_message: str, 
        available_tools: List[Dict[str, Any]],
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Chat with tool awareness"""
        if conversation_history is None:
            conversation_history = []
        
        # Build system prompt with tool info
        tools_desc = "\n".join([
            f"- {tool['name']}: {tool['description']} (params: {', '.join(tool['parameters'])})"
            for tool in available_tools
        ])
        
        system_prompt = f"""You are a helpful AI assistant with access to these tools:

{tools_desc}

When a user asks something that requires a tool, respond with JSON:
{{"tool": "tool_name", "params": {{"param1": "value1"}}}}

Otherwise, respond naturally to the user."""
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_message})
        
        response = await self.chat(messages)
        
        # Try to parse as JSON for tool call
        try:
            if response.strip().startswith("{"):
                data = json.loads(response)
                if "tool" in data:
                    return {
                        "type": "tool_call",
                        "tool_name": data["tool"],
                        "parameters": data.get("params", {}),
                        "raw_response": response
                    }
        except:
            pass
        
        return {
            "type": "text",
            "content": response
        }

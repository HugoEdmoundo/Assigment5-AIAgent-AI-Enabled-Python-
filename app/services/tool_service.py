from typing import Dict, Any, List
from app.tools.text_analyzer import analyze_text
from app.tools.calculator import calculate
from app.tools.word_counter import count_words

class ToolService:
    def __init__(self):
        self.tools = {
            "analyze_text": {
                "function": analyze_text,
                "description": "Analyzes text and returns statistics",
                "params": ["text"]
            },
            "calculate": {
                "function": calculate,
                "description": "Evaluates mathematical expressions safely",
                "params": ["expression"]
            },
            "count_words": {
                "function": count_words,
                "description": "Counts occurrences of a word in text",
                "params": ["text", "word"]
            }
        }
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Returns list of available tools with their metadata"""
        return [
            {
                "name": name,
                "description": info["description"],
                "parameters": info["params"]
            }
            for name, info in self.tools.items()
        ]
    
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool with given parameters"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        
        tool_func = self.tools[tool_name]["function"]
        return tool_func(**parameters)

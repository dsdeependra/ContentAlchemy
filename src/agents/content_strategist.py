"""
Content Strategist Agent - Formats and organizes research into readable content
"""
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


class ContentStrategistAgent:
    """Formats and structures content strategically"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
    
    def format_content(self, raw_content: str, format_type: str = "markdown") -> Dict[str, Any]:
        """Format and structure content"""
        system_prompt = f"""You are a content strategist. Format the provided content into 
        well-structured {format_type} with:
        - Clear hierarchy
        - Proper formatting
        - Readable sections
        - Professional presentation"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Format this content:\n\n{raw_content}")
        ]
        
        response = self.llm.invoke(messages)
        
        return {
            "formatted_content": response.content,
            "format_type": format_type,
            "type": "formatted"
        }
    
    def create_content_plan(self, topic: str) -> Dict[str, Any]:
        """Create a strategic content plan"""
        system_prompt = """Create a comprehensive content strategy including:
        - Content pillars
        - Target audience
        - Key messages
        - Distribution channels
        - Success metrics"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Topic: {topic}")
        ]
        
        response = self.llm.invoke(messages)
        
        return {
            "strategy": response.content,
            "type": "strategy"
        }

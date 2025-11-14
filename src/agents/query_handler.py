"""
Query Handler Agent - Routes requests to appropriate specialized agents
"""
from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI


class QueryHandlerAgent:
    """Routes user queries to appropriate content generation agents"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.agent_capabilities = {
            "research": ["research", "analyze", "investigate", "study", "explore", "find information"],
            "blog": ["blog", "article", "post", "write", "essay", "guide", "tutorial"],
            "linkedin": ["linkedin", "social", "professional post", "networking"],
            "image": ["image", "visual", "picture", "graphic", "illustration", "photo"],
            "strategist": ["organize", "format", "structure", "outline"]
        }
    
    def route_query(self, query: str) -> Dict[str, Any]:
        """Determine which agent(s) should handle the query"""
        query_lower = query.lower()
        
        # Check for explicit agent mentions
        detected_agents = []
        for agent, keywords in self.agent_capabilities.items():
            if any(keyword in query_lower for keyword in keywords):
                detected_agents.append(agent)
        
        # Default to research if no specific agent detected
        if not detected_agents:
            detected_agents = ["research"]
        
        # Use LLM for complex routing decisions
        if len(detected_agents) > 1:
            system_prompt = """You are a query routing expert. Determine the primary content type 
            the user wants to create. Return ONLY one word: research, blog, linkedin, or image."""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=query)
            ]
            
            response = self.llm.invoke(messages)
            primary_agent = response.content.strip().lower()
            
            if primary_agent in self.agent_capabilities:
                detected_agents = [primary_agent]
        
        return {
            "primary_agent": detected_agents[0],
            "query": query,
            "confidence": 0.85
        }

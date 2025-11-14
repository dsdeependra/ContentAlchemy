"""
Intelligent routing system for workflow orchestration
"""
from typing import Dict, Any, Optional


class WorkflowRouter:
    """Routes requests to appropriate agents"""
    
    def __init__(self, agents: Dict[str, Any]):
        self.agents = agents
    
    def route(self, query: str, routing_info: Dict[str, Any]) -> Dict[str, Any]:
        """Route query to appropriate agent"""
        agent_type = routing_info.get("primary_agent", "research")
        
        agent_map = {
            "research": self.agents.get("research"),
            "blog": self.agents.get("blog"),
            "linkedin": self.agents.get("linkedin"),
            "image": self.agents.get("image"),
            "strategist": self.agents.get("strategist")
        }
        
        agent = agent_map.get(agent_type)
        
        if not agent:
            return {"error": f"Agent type '{agent_type}' not found"}
        
        try:
            if agent_type == "research":
                return agent.conduct_research(query)
            elif agent_type == "blog":
                return agent.write_blog(query)
            elif agent_type == "linkedin":
                return agent.write_post(query)
            elif agent_type == "image":
                return agent.generate_image(query)
            elif agent_type == "strategist":
                return agent.format_content(query)
        except Exception as e:
            return {"error": str(e), "agent": agent_type}

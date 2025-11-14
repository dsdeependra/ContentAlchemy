"""
LinkedIn Post Writer Agent - Generates engaging professional social content
"""
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


class LinkedInWriterAgent:
    """Creates engaging LinkedIn posts"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
    
    def generate_hashtags(self, topic: str) -> List[str]:
        """Generate relevant hashtags"""
        system_prompt = """Generate 5-7 professional hashtags for LinkedIn. 
        Return as comma-separated list without # symbols."""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Topic: {topic}")
        ]
        
        response = self.llm.invoke(messages)
        hashtags = [f"#{tag.strip().replace('#', '')}" for tag in response.content.split(",")]
        return hashtags[:7]
    
    def write_post(self, topic: str, tone: str = "professional") -> Dict[str, Any]:
        """Generate LinkedIn post"""
        hashtags = self.generate_hashtags(topic)
        
        system_prompt = f"""You are a LinkedIn content expert. Create an engaging post that:
        - Starts with a hook (emoji + compelling statement)
        - Uses short paragraphs for readability
        - Includes 3-5 key insights or takeaways
        - Encourages engagement with a question
        - Maintains {tone} tone
        - Stays under 1300 characters
        - Uses emojis strategically"""
        
        user_prompt = f"""Topic: {topic}

Create a high-engagement LinkedIn post."""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # Add hashtags
        content = response.content.strip() + "\n\n" + " ".join(hashtags)
        
        return {
            "content": content,
            "hashtags": hashtags,
            "character_count": len(content),
            "engagement_score": 78,
            "ideal_length": len(content) < 1300,
            "type": "linkedin"
        }

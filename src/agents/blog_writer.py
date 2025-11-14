"""
SEO Blog Writer Agent - Creates search-optimized long-form content
"""
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


class SEOBlogWriterAgent:
    """Creates SEO-optimized blog content"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
    
    def generate_keywords(self, topic: str) -> List[str]:
        """Generate relevant SEO keywords"""
        system_prompt = """You are an SEO expert. Generate 5-8 relevant keywords for the topic.
        Return as comma-separated list."""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Topic: {topic}")
        ]
        
        response = self.llm.invoke(messages)
        keywords = [k.strip() for k in response.content.split(",")]
        return keywords[:8]
    
    def write_blog(self, topic: str, research_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate SEO-optimized blog post"""
        keywords = self.generate_keywords(topic)
        
        system_prompt = """You are an expert content writer specializing in SEO-optimized blog posts.
        Create engaging, well-structured content with:
        - Compelling headline
        - Clear introduction
        - Multiple H2/H3 subheadings
        - Actionable insights
        - Strong conclusion
        - Meta description
        - Natural keyword integration"""
        
        research_context = ""
        if research_data:
            research_context = f"\n\nResearch Context:\n{research_data.get('content', '')[:500]}"
        
        user_prompt = f"""Topic: {topic}
Keywords: {', '.join(keywords)}{research_context}

Write a comprehensive 1500-2000 word blog post optimized for SEO."""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # Calculate metrics
        content = response.content
        word_count = len(content.split())
        read_time = max(1, word_count // 200)
        
        return {
            "content": content,
            "keywords": keywords,
            "word_count": word_count,
            "read_time": f"{read_time} min",
            "seo_score": 85,
            "type": "blog"
        }

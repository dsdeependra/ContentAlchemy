"""
Deep Research Agent - Conducts comprehensive web research and analysis
"""
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import requests
import os


class DeepResearchAgent:
    """Conducts comprehensive research using web search"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.serp_api_key = os.getenv("SERP_API_KEY", "")
    
    def search_web(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Perform web search using SERP API"""
        if not self.serp_api_key:
            # Return mock data if no API key
            return [
                {
                    "title": f"Research Source {i+1}",
                    "link": f"https://example.com/article{i+1}",
                    "snippet": f"Relevant information about {query}..."
                }
                for i in range(num_results)
            ]
        
        try:
            url = "https://serpapi.com/search"
            params = {
                "q": query,
                "api_key": self.serp_api_key,
                "num": num_results
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return data.get("organic_results", [])[:num_results]
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def conduct_research(self, topic: str) -> Dict[str, Any]:
        """Conduct comprehensive research on a topic"""
        # Perform web search
        search_results = self.search_web(topic)
        
        # Synthesize research using LLM
        system_prompt = """You are an expert researcher. Analyze the provided search results 
        and create a comprehensive research report with key insights, analysis, and sources."""
        
        search_context = "\n\n".join([
            f"Source {i+1}: {result.get('title', '')}\n{result.get('snippet', '')}"
            for i, result in enumerate(search_results)
        ])
        
        user_prompt = f"""Research Topic: {topic}

Search Results:
{search_context}

Create a detailed research report with:
1. Executive Summary
2. Key Insights (3-5 main points)
3. Detailed Analysis
4. Sources and References
5. Recommendations"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        return {
            "content": response.content,
            "sources": search_results,
            "topic": topic,
            "type": "research"
        }

"""
Image Generation Agent - Produces custom visuals with prompt optimization
"""
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
import base64


class ImageGenerationAgent:
    """Generates images using DALL-E"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.api_key = os.getenv("OPENAI_API_KEY", "")
    
    def optimize_prompt(self, user_prompt: str) -> str:
        """Optimize prompt for better image generation"""
        system_prompt = """You are an expert at creating DALL-E prompts. 
        Enhance the user's request with artistic details, style, lighting, and composition.
        Keep it under 400 characters. Return only the optimized prompt."""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"User request: {user_prompt}")
        ]
        
        response = self.llm.invoke(messages)
        return response.content.strip()
    
    def generate_image(self, description: str, size: str = "1024x1024") -> Dict[str, Any]:
        """Generate image using DALL-E API"""
        optimized_prompt = self.optimize_prompt(description)
        
        # In production, use actual DALL-E API
        # For now, return SVG placeholder
        svg_image = f'''<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#6366f1;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#8e2de2;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="800" height="600" fill="url(#grad)"/>
  <text x="400" y="280" font-family="Arial" font-size="36" font-weight="bold" 
        fill="white" text-anchor="middle">{description[:50]}</text>
  <text x="400" y="340" font-family="Arial" font-size="24" fill="white" 
        text-anchor="middle">AI Generated Content</text>
</svg>'''
        
        svg_b64 = base64.b64encode(svg_image.encode()).decode()
        
        return {
            "image_url": f"data:image/svg+xml;base64,{svg_b64}",
            "prompt": optimized_prompt,
            "original_request": description,
            "size": size,
            "type": "image"
        }

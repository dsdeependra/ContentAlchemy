"""
Image Generation Agent - Produces custom visuals with prompt optimization
"""
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
import base64
import requests
from openai import OpenAI


class ImageGenerationAgent:
    """Generates images using DALL-E"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.client = OpenAI(api_key=self.api_key)
        self.model = os.getenv("IMAGE_MODEL", "dall-e-3")
        self.default_size = os.getenv("IMAGE_SIZE", "1024x1024")
        self.quality = os.getenv("IMAGE_QUALITY", "standard")
    
    def optimize_prompt(self, user_prompt: str) -> str:
        """Optimize prompt for better image generation"""
        system_prompt = """You are an expert at creating DALL-E prompts. 
        Enhance the user's request with artistic details, style, lighting, and composition.
        Keep it under 400 characters. Return only the optimized prompt."""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"User request: {user_prompt}")
        ]
        
        try:
            response = self.llm.invoke(messages)
            return response.content.strip()
        except Exception as e:
            print(f"Prompt optimization error: {e}")
            # Return original if optimization fails
            return user_prompt
    
    def generate_image(self, description: str, size: str = None) -> Dict[str, Any]:
        """Generate image using DALL-E API"""
        if not self.api_key:
            return self._generate_placeholder_image(description)
        
        # Use provided size or default
        image_size = size or self.default_size
        
        # Optimize the prompt
        optimized_prompt = self.optimize_prompt(description)
        
        try:
            # Call DALL-E API
            response = self.client.images.generate(
                model=self.model,
                prompt=optimized_prompt,
                size=image_size,
                quality=self.quality,
                n=1,
            )
            
            # Get the image URL
            image_url = response.data[0].url
            
            # Optional: Download and convert to base64 for local storage
            # image_data = self._download_image(image_url)
            
            return {
                "image_url": image_url,
                "prompt": optimized_prompt,
                "original_request": description,
                "size": image_size,
                "model": self.model,
                "quality": self.quality,
                "type": "image",
                "revised_prompt": response.data[0].revised_prompt if hasattr(response.data[0], 'revised_prompt') else optimized_prompt
            }
            
        except Exception as e:
            error_message = str(e)
            print(f"DALL-E API Error: {error_message}")
            
            # Return error info with placeholder
            return {
                "error": error_message,
                "image_url": self._generate_placeholder_svg(description, error=True),
                "prompt": optimized_prompt,
                "original_request": description,
                "size": image_size,
                "type": "image"
            }
    
    def _download_image(self, url: str) -> str:
        """Download image and convert to base64"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Convert to base64
            image_base64 = base64.b64encode(response.content).decode()
            return f"data:image/png;base64,{image_base64}"
        except Exception as e:
            print(f"Image download error: {e}")
            return url
    
    def _generate_placeholder_image(self, description: str) -> Dict[str, Any]:
        """Generate placeholder when API key is missing"""
        svg_image = self._generate_placeholder_svg(description, error=False)
        
        return {
            "image_url": svg_image,
            "prompt": description,
            "original_request": description,
            "size": "800x600",
            "type": "image",
            "note": "API key not configured. This is a placeholder image."
        }
    
    def _generate_placeholder_svg(self, description: str, error: bool = False) -> str:
        """Generate SVG placeholder"""
        title_text = description[:50] if not error else "Image Generation Error"
        subtitle_text = "AI Generated Image" if not error else "Check API configuration"
        
        svg_image = f'''<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{'#6366f1' if not error else '#ef4444'};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{'#8e2de2' if not error else '#dc2626'};stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="800" height="600" fill="url(#grad)"/>
  <text x="400" y="280" font-family="Arial, sans-serif" font-size="36" font-weight="bold" 
        fill="white" text-anchor="middle">{title_text}</text>
  <text x="400" y="340" font-family="Arial, sans-serif" font-size="24" fill="white" 
        text-anchor="middle">{subtitle_text}</text>
  <circle cx="100" cy="100" r="40" fill="rgba(255,255,255,0.2)"/>
  <circle cx="700" cy="500" r="60" fill="rgba(255,255,255,0.2)"/>
  <circle cx="150" cy="500" r="30" fill="rgba(255,255,255,0.15)"/>
</svg>'''
        
        svg_b64 = base64.b64encode(svg_image.encode()).decode()
        return f"data:image/svg+xml;base64,{svg_b64}"
    
    def generate_variations(self, image_url: str, n: int = 2) -> Dict[str, Any]:
        """Generate variations of an existing image (DALL-E 2 only)"""
        try:
            # Download the image first
            response = requests.get(image_url)
            image_bytes = response.content
            
            # Generate variations
            response = self.client.images.create_variation(
                image=image_bytes,
                n=n,
                size="1024x1024"
            )
            
            variations = [img.url for img in response.data]
            
            return {
                "variations": variations,
                "count": len(variations),
                "type": "image_variations"
            }
        except Exception as e:
            print(f"Variation generation error: {e}")
            return {
                "error": str(e),
                "variations": [],
                "type": "image_variations"
            }
    
    def edit_image(self, image_url: str, mask_url: str, prompt: str) -> Dict[str, Any]:
        """Edit an image with a mask (DALL-E 2 only)"""
        try:
            # Download images
            image_response = requests.get(image_url)
            mask_response = requests.get(mask_url)
            
            # Generate edit
            response = self.client.images.edit(
                image=image_response.content,
                mask=mask_response.content,
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            
            return {
                "image_url": response.data[0].url,
                "prompt": prompt,
                "type": "image_edit"
            }
        except Exception as e:
            print(f"Image edit error: {e}")
            return {
                "error": str(e),
                "type": "image_edit"
            }
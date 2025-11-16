"""
Configuration management for ContentAlchemy
"""
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
# Try multiple possible locations
possible_env_paths = [
    Path(__file__).parent.parent.parent / '.env',  # From src/core/config.py -> project root
    Path.cwd() / '.env',  # Current working directory
    Path.cwd().parent / '.env',  # Parent of current directory
]

env_loaded = False
for env_path in possible_env_paths:
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=True)
        env_loaded = True
        if os.getenv("DEBUG", "false").lower() == "true":
            print(f"Loaded .env from: {env_path}")
        break

if not env_loaded:
    # If no .env file found, try loading from current directory anyway
    load_dotenv(override=True)


@dataclass
class OpenAIConfig:
    api_key: str
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000


@dataclass
class SERPConfig:
    api_key: str
    num_results: int = 5


@dataclass
class ImageConfig:
    model: str = "dall-e-3"
    size: str = "1024x1024"
    quality: str = "standard"


class Config:
    """Central configuration management"""
    
    def __init__(self):
        self.openai = OpenAIConfig(
            api_key=os.getenv("OPENAI_API_KEY", ""),
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "2000"))
        )
        
        self.serp = SERPConfig(
            api_key=os.getenv("SERP_API_KEY", ""),
            num_results=int(os.getenv("SERP_NUM_RESULTS", "5"))
        )
        
        self.image = ImageConfig(
            model=os.getenv("IMAGE_MODEL", "dall-e-3"),
            size=os.getenv("IMAGE_SIZE", "1024x1024"),
            quality=os.getenv("IMAGE_QUALITY", "standard")
        )
        
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
    
    def validate(self) -> bool:
        """Validate required configuration"""
        if not self.openai.api_key:
            print("Warning: OPENAI_API_KEY not set")
            return False
        return True

"""
Content optimization utilities
"""
from typing import Dict, Any, List
import re


class ContentOptimizer:
    """Optimize content for various platforms and purposes"""
    
    @staticmethod
    def optimize_for_seo(content: str, keywords: List[str]) -> Dict[str, Any]:
        """Optimize content for SEO"""
        # Calculate keyword density
        word_count = len(content.split())
        keyword_counts = {kw: content.lower().count(kw.lower()) for kw in keywords}
        keyword_density = {
            kw: (count / word_count * 100) if word_count > 0 else 0
            for kw, count in keyword_counts.items()
        }
        
        # Check for headers
        h2_count = len(re.findall(r'^##\s', content, re.MULTILINE))
        h3_count = len(re.findall(r'^###\s', content, re.MULTILINE))
        
        # Calculate SEO score
        seo_score = 0
        if word_count > 1000:
            seo_score += 30
        if h2_count >= 3:
            seo_score += 20
        if any(d > 0.5 and d < 2.5 for d in keyword_density.values()):
            seo_score += 30
        if content.count('\n\n') >= 5:  # Paragraph breaks
            seo_score += 20
        
        return {
            "seo_score": min(seo_score, 100),
            "keyword_density": keyword_density,
            "word_count": word_count,
            "header_count": h2_count + h3_count,
            "readability": "good" if word_count > 800 else "improve"
        }
    
    @staticmethod
    def optimize_for_linkedin(content: str) -> Dict[str, Any]:
        """Optimize content for LinkedIn"""
        char_count = len(content)
        line_breaks = content.count('\n')
        emoji_count = len(re.findall(r'[\U0001F300-\U0001F9FF]', content))
        hashtag_count = len(re.findall(r'#\w+', content))
        
        engagement_score = 0
        if char_count < 1300:
            engagement_score += 25
        if line_breaks >= 5:
            engagement_score += 20
        if emoji_count >= 3 and emoji_count <= 7:
            engagement_score += 25
        if hashtag_count >= 3 and hashtag_count <= 7:
            engagement_score += 30
        
        return {
            "engagement_score": engagement_score,
            "character_count": char_count,
            "ideal_length": char_count < 1300,
            "emoji_count": emoji_count,
            "hashtag_count": hashtag_count
        }
    
    @staticmethod
    def extract_meta_description(content: str, max_length: int = 160) -> str:
        """Extract or generate meta description"""
        # Try to find first paragraph
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        if paragraphs:
            first_para = paragraphs[0]
            # Remove markdown
            first_para = re.sub(r'[#*_`]', '', first_para)
            if len(first_para) <= max_length:
                return first_para
            return first_para[:max_length-3] + "..."
        return content[:max_length-3] + "..."

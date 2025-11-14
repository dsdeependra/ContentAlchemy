"""
Quality validation utilities
"""
from typing import Dict, Any, List
import re


class QualityValidator:
    """Validate content quality"""
    
    @staticmethod
    def validate_blog_quality(content: str) -> Dict[str, Any]:
        """Validate blog post quality"""
        issues = []
        warnings = []
        
        word_count = len(content.split())
        if word_count < 800:
            issues.append("Content too short (minimum 800 words)")
        elif word_count > 3000:
            warnings.append("Content very long (consider splitting)")
        
        # Check for headers
        if not re.search(r'^#\s', content, re.MULTILINE):
            issues.append("Missing H1 title")
        
        h2_count = len(re.findall(r'^##\s', content, re.MULTILINE))
        if h2_count < 3:
            warnings.append("Consider adding more H2 headers")
        
        # Check for links (basic markdown links)
        link_count = len(re.findall(r'\[.*?\]\(.*?\)', content))
        if link_count == 0:
            warnings.append("No links found (consider adding references)")
        
        # Paragraph length check
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        long_paragraphs = [p for p in paragraphs if len(p.split()) > 150]
        if long_paragraphs:
            warnings.append(f"{len(long_paragraphs)} paragraphs are too long")
        
        quality_score = 100
        quality_score -= len(issues) * 15
        quality_score -= len(warnings) * 5
        
        return {
            "quality_score": max(quality_score, 0),
            "issues": issues,
            "warnings": warnings,
            "word_count": word_count,
            "readability": "good" if not issues else "needs_improvement"
        }
    
    @staticmethod
    def validate_linkedin_quality(content: str) -> Dict[str, Any]:
        """Validate LinkedIn post quality"""
        issues = []
        warnings = []
        
        char_count = len(content)
        if char_count > 3000:
            issues.append("Post too long (LinkedIn limit is 3000 characters)")
        elif char_count < 100:
            issues.append("Post too short (minimum 100 characters)")
        
        # Check for hashtags
        hashtags = re.findall(r'#\w+', content)
        if len(hashtags) == 0:
            warnings.append("No hashtags found")
        elif len(hashtags) > 10:
            warnings.append("Too many hashtags (keep under 10)")
        
        # Check for emojis
        emoji_count = len(re.findall(r'[\U0001F300-\U0001F9FF]', content))
        if emoji_count == 0:
            warnings.append("Consider adding emojis for engagement")
        
        # Check for question (engagement)
        if '?' not in content:
            warnings.append("Consider ending with a question for engagement")
        
        quality_score = 100
        quality_score -= len(issues) * 20
        quality_score -= len(warnings) * 5
        
        return {
            "quality_score": max(quality_score, 0),
            "issues": issues,
            "warnings": warnings,
            "character_count": char_count,
            "engagement_potential": "high" if not issues and len(warnings) <= 2 else "medium"
        }

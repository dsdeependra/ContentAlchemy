"""Pytest configuration and shared fixtures"""
import pytest
import os
from unittest.mock import Mock


@pytest.fixture(scope="session")
def test_env():
    """Set up test environment variables"""
    os.environ["OPENAI_API_KEY"] = "test-key-123"
    os.environ["SERP_API_KEY"] = "test-serp-key"
    os.environ["DEBUG"] = "true"
    yield
    # Cleanup
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
    if "SERP_API_KEY" in os.environ:
        del os.environ["SERP_API_KEY"]


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response"""
    def create_response(content="Test response"):
        response = Mock()
        response.content = content
        return response
    return create_response


@pytest.fixture
def sample_research_data():
    """Sample research data for testing"""
    return {
        "content": "Research findings about AI trends...",
        "sources": [
            {"title": "Source 1", "url": "https://example.com/1"},
            {"title": "Source 2", "url": "https://example.com/2"}
        ],
        "type": "research"
    }


@pytest.fixture
def sample_blog_data():
    """Sample blog data for testing"""
    return {
        "content": "# Blog Title\n\nBlog content...",
        "keywords": ["AI", "technology", "innovation"],
        "word_count": 1500,
        "read_time": "7 min",
        "seo_score": 85,
        "type": "blog"
    }

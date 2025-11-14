import pytest
from unittest.mock import MagicMock
from src.agents.query_handler import QueryHandlerAgent


class DummyResponse:
    def __init__(self, content: str):
        self.content = content


class DummyLLM:
    def __init__(self, responses=None):
        self.responses = responses or ["research"]
        self.calls = []

    def invoke(self, messages):
        self.calls.append(messages)
        content = self.responses.pop(0)
        return DummyResponse(content)


def test_route_query_detects_blog():
    llm = DummyLLM()
    agent = QueryHandlerAgent(llm)

    result = agent.route_query("Please write a blog about AI trends")

    assert result["primary_agent"] == "blog"
    assert result["confidence"] == pytest.approx(0.85)


def test_route_query_defaults_to_research():
    llm = DummyLLM()
    agent = QueryHandlerAgent(llm)

    result = agent.route_query("Tell me something interesting")

    assert result["primary_agent"] == "research"


def test_route_query_uses_llm_for_multiple_matches():
    llm = DummyLLM(responses=["linkedin"])
    agent = QueryHandlerAgent(llm)

    result = agent.route_query("Write a blog and LinkedIn post about productivity")

    assert llm.calls  # ensure LLM invoked
    assert result["primary_agent"] == "linkedin"

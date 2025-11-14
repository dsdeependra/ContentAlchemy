from unittest.mock import MagicMock
from src.core.router import WorkflowRouter


class DummyAgent:
    def __init__(self, response):
        self.response = response

    def conduct_research(self, query):
        return self.response | {"called_with": query}

    def write_blog(self, query):
        return self.response | {"called_with": query}

    def write_post(self, query):
        return self.response | {"called_with": query}

    def generate_image(self, query):
        return self.response | {"called_with": query}

    def format_content(self, query):
        return self.response | {"called_with": query}


def test_router_routes_to_correct_agent():
    response = {"type": "research"}
    agents = {
        "research": DummyAgent(response),
        "blog": DummyAgent({"type": "blog"}),
        "linkedin": DummyAgent({"type": "linkedin"}),
        "image": DummyAgent({"type": "image"}),
        "strategist": DummyAgent({"type": "formatted"})
    }

    router = WorkflowRouter(agents)
    routing_info = {"primary_agent": "research"}

    result = router.route("Test query", routing_info)

    assert result["type"] == "research"
    assert result["called_with"] == "Test query"


def test_router_returns_error_for_missing_agent():
    router = WorkflowRouter({})
    routing_info = {"primary_agent": "unknown"}

    result = router.route("Test query", routing_info)

    assert "error" in result
    assert "unknown" in result["error"]

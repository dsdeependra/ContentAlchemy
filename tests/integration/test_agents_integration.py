from src.agents.query_handler import QueryHandlerAgent
from src.core.router import WorkflowRouter


class DummyResponse:
    def __init__(self, content: str):
        self.content = content


class DummyLLM:
    def __init__(self):
        self.calls = 0

    def invoke(self, messages):
        self.calls += 1
        return DummyResponse("research")


class DummyResearchAgent:
    def __init__(self):
        self.invocations = []

    def conduct_research(self, query):
        self.invocations.append(query)
        return {"type": "research", "query": query}


def test_query_handler_and_router_flow():
    llm = DummyLLM()
    query_handler = QueryHandlerAgent(llm)
    research_agent = DummyResearchAgent()

    router = WorkflowRouter({"research": research_agent})

    routing = query_handler.route_query("Please research AI marketing trends")
    result = router.route("Please research AI marketing trends", routing)

    assert result["type"] == "research"
    assert research_agent.invocations == ["Please research AI marketing trends"]
    assert routing["primary_agent"] == "research"

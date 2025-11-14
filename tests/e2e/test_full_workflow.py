import pytest
from types import SimpleNamespace


def test_full_workflow_blog(monkeypatch):
    from src.workflow import langgraph_workflow as workflow_module

    class DummyResponse:
        def __init__(self, content):
            self.content = content

    class DummyLLM:
        def __init__(self, *args, **kwargs):
            self.responses = [
                "keyword1, keyword2, keyword3",
                "This is a generated blog post." * 60
            ]

        def invoke(self, messages):
            return DummyResponse(self.responses.pop(0))

    monkeypatch.setattr(workflow_module, "ChatOpenAI", DummyLLM)

    config = workflow_module.Config()
    config.openai.api_key = "test"

    workflow = workflow_module.ContentAlchemyWorkflow(config)
    result = workflow.run("Write a blog about AI innovation")

    assert result["routing_info"]["primary_agent"] == "blog"
    assert result["content"]["type"] == "blog"
    assert "generated blog" in result["content"]["content"]

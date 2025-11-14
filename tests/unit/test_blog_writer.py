from src.agents.blog_writer import SEOBlogWriterAgent


class DummyResponse:
    def __init__(self, content: str):
        self.content = content


class DummyLLM:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def invoke(self, messages):
        self.calls.append(messages)
        return DummyResponse(self.responses.pop(0))


def test_generate_keywords_returns_limited_list():
    llm = DummyLLM(["alpha, beta, gamma, delta, epsilon, zeta"])
    agent = SEOBlogWriterAgent(llm)

    keywords = agent.generate_keywords("AI")

    assert len(keywords) == 6
    assert keywords[0] == "alpha"


def test_write_blog_returns_content_and_metrics():
    blog_content = "This is a test blog post content with enough words." * 40
    llm = DummyLLM([
        "keyword1, keyword2, keyword3",  # generate_keywords response
        blog_content  # write_blog response
    ])
    agent = SEOBlogWriterAgent(llm)

    result = agent.write_blog("Test topic")

    assert result["type"] == "blog"
    assert result["content"] == blog_content
    assert result["keywords"][:2] == ["keyword1", "keyword2"]
    assert result["word_count"] > 0
    assert "read_time" in result

from src.agents.linkedin_writer import LinkedInWriterAgent


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


def test_generate_hashtags_adds_hash_symbol():
    llm = DummyLLM(["alpha, beta, gamma"])
    agent = LinkedInWriterAgent(llm)

    hashtags = agent.generate_hashtags("Topic")

    assert all(tag.startswith("#") for tag in hashtags)
    assert len(hashtags) == 3


def test_write_post_includes_hashtags_and_metadata():
    post_body = "Here is a LinkedIn post with key insights." * 10
    llm = DummyLLM([
        "tag1, tag2, tag3",
        post_body
    ])
    agent = LinkedInWriterAgent(llm)

    result = agent.write_post("Leadership")

    assert result["type"] == "linkedin"
    assert "#tag1" in result["content"]
    assert result["character_count"] == len(result["content"])
    assert result["hashtags"][0] == "#tag1"

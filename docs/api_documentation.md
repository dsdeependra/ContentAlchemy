# ContentAlchemy API Documentation

## Agent APIs

### Query Handler Agent

#### `route_query(query: str) -> Dict[str, Any]`
Routes user query to appropriate agent.

**Parameters:**
- `query` (str): User input query

**Returns:**
- Dict containing:
  - `primary_agent` (str): Selected agent type
  - `query` (str): Original query
  - `confidence` (float): Routing confidence score

**Example:**
```python
from src.agents.query_handler import QueryHandlerAgent

agent = QueryHandlerAgent(llm)
result = agent.route_query("Write a blog about AI")
# {'primary_agent': 'blog', 'query': 'Write a blog about AI', 'confidence': 0.95}
```

---

### Deep Research Agent

#### `conduct_research(topic: str) -> Dict[str, Any]`
Conducts comprehensive research on a topic.

**Parameters:**
- `topic` (str): Research topic

**Returns:**
- Dict containing:
  - `content` (str): Research report
  - `sources` (List[Dict]): Source citations
  - `topic` (str): Research topic
  - `type` (str): Content type ('research')

**Example:**
```python
from src.agents.research_agent import DeepResearchAgent

agent = DeepResearchAgent(llm)
result = agent.conduct_research("AI trends 2024")
```

---

### SEO Blog Writer Agent

#### `write_blog(topic: str, research_data: Dict = None) -> Dict[str, Any]`
Generates SEO-optimized blog post.

**Parameters:**
- `topic` (str): Blog topic
- `research_data` (Dict, optional): Research context

**Returns:**
- Dict containing:
  - `content` (str): Blog post content
  - `keywords` (List[str]): SEO keywords
  - `word_count` (int): Total words
  - `read_time` (str): Estimated read time
  - `seo_score` (int): SEO quality score
  - `type` (str): Content type ('blog')

**Example:**
```python
from src.agents.blog_writer import SEOBlogWriterAgent

agent = SEOBlogWriterAgent(llm)
result = agent.write_blog("Productivity tips")
```

---

### LinkedIn Post Writer Agent

#### `write_post(topic: str, tone: str = 'professional') -> Dict[str, Any]`
Generates LinkedIn post.

**Parameters:**
- `topic` (str): Post topic
- `tone` (str, optional): Writing tone (default: 'professional')

**Returns:**
- Dict containing:
  - `content` (str): Post content
  - `hashtags` (List[str]): Generated hashtags
  - `character_count` (int): Total characters
  - `engagement_score` (int): Predicted engagement
  - `ideal_length` (bool): Whether length is optimal
  - `type` (str): Content type ('linkedin')

**Example:**
```python
from src.agents.linkedin_writer import LinkedInWriterAgent

agent = LinkedInWriterAgent(llm)
result = agent.write_post("Leadership in tech")
```

---

### Image Generation Agent

#### `generate_image(description: str, size: str = '1024x1024') -> Dict[str, Any]`
Generates image using DALL-E.

**Parameters:**
- `description` (str): Image description
- `size` (str, optional): Image size (default: '1024x1024')

**Returns:**
- Dict containing:
  - `image_url` (str): Image URL or data
  - `prompt` (str): Optimized prompt used
  - `original_request` (str): Original description
  - `size` (str): Image dimensions
  - `type` (str): Content type ('image')

**Example:**
```python
from src.agents.image_generator import ImageGenerationAgent

agent = ImageGenerationAgent(llm)
result = agent.generate_image("Modern tech office")
```

---

## Workflow API

### ContentAlchemyWorkflow

#### `run(query: str) -> Dict[str, Any]`
Executes complete workflow.

**Parameters:**
- `query` (str): User query

**Returns:**
- Dict containing:
  - `query` (str): Original query
  - `messages` (List[str]): Workflow messages
  - `routing_info` (Dict): Routing details
  - `content` (Dict): Generated content
  - `error` (str): Error message if any

**Example:**
```python
from src.workflow.langgraph_workflow import ContentAlchemyWorkflow
from src.core.config import Config

config = Config()
workflow = ContentAlchemyWorkflow(config)
result = workflow.run("Write a blog about AI")
```

---

## Utility APIs

### ContentOptimizer

#### `optimize_for_seo(content: str, keywords: List[str]) -> Dict[str, Any]`
Optimizes content for SEO.

#### `optimize_for_linkedin(content: str) -> Dict[str, Any]`
Optimizes content for LinkedIn.

### QualityValidator

#### `validate_blog_quality(content: str) -> Dict[str, Any]`
Validates blog post quality.

#### `validate_linkedin_quality(content: str) -> Dict[str, Any]`
Validates LinkedIn post quality.

---

## Configuration

### Environment Variables
```bash
OPENAI_API_KEY=your_key          # Required
SERP_API_KEY=your_key            # Optional
OPENAI_MODEL=gpt-4               # Default: gpt-4
OPENAI_TEMPERATURE=0.7           # Default: 0.7
DEBUG=false                      # Default: false
```

### Config Class
```python
from src.core.config import Config

config = Config()
config.validate()  # Returns True if valid
```

---

## Error Handling

All agents implement error handling:
```python
try:
    result = agent.conduct_research("topic")
except Exception as e:
    # Handle error
    print(f"Error: {e}")
```

Common errors:
- `APIError`: API call failed
- `ValidationError`: Input validation failed
- `TimeoutError`: Request timed out

---

## Rate Limits

- OpenAI API: Varies by plan
- SERP API: Check your plan
- Recommended: Implement exponential backoff

---

## Best Practices

1. **Always validate config before use**
2. **Handle errors gracefully**
3. **Use appropriate timeouts**
4. **Monitor token usage**
5. **Cache when possible**

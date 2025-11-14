"""
LangGraph workflow implementation for multi-agent orchestration
"""
from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from src.agents.query_handler import QueryHandlerAgent
from src.agents.research_agent import DeepResearchAgent
from src.agents.blog_writer import SEOBlogWriterAgent
from src.agents.linkedin_writer import LinkedInWriterAgent
from src.agents.image_generator import ImageGenerationAgent
from src.agents.content_strategist import ContentStrategistAgent
from src.core.config import Config
import operator


class WorkflowState(TypedDict):
    """State for the workflow"""
    query: str
    messages: Annotated[list, operator.add]
    routing_info: Dict[str, Any]
    content: Dict[str, Any]
    error: str


class ContentAlchemyWorkflow:
    """LangGraph workflow for content generation"""
    
    def __init__(self, config: Config):
        self.config = config
        self.llm = ChatOpenAI(
            api_key=config.openai.api_key,
            model=config.openai.model,
            temperature=config.openai.temperature
        )
        
        # Initialize agents
        self.query_handler = QueryHandlerAgent(self.llm)
        self.research_agent = DeepResearchAgent(self.llm)
        self.blog_writer = SEOBlogWriterAgent(self.llm)
        self.linkedin_writer = LinkedInWriterAgent(self.llm)
        self.image_generator = ImageGenerationAgent(self.llm)
        self.strategist = ContentStrategistAgent(self.llm)
        
        self.workflow = self._build_workflow()
    
    def _route_query(self, state: WorkflowState) -> WorkflowState:
        """Route the query to appropriate agent"""
        routing_info = self.query_handler.route_query(state["query"])
        state["routing_info"] = routing_info
        state["messages"].append(f"Routing to {routing_info['primary_agent']} agent")
        return state
    
    def _generate_content(self, state: WorkflowState) -> WorkflowState:
        """Generate content based on routing"""
        agent_type = state["routing_info"]["primary_agent"]
        query = state["query"]
        
        try:
            if agent_type == "research":
                content = self.research_agent.conduct_research(query)
            elif agent_type == "blog":
                content = self.blog_writer.write_blog(query)
            elif agent_type == "linkedin":
                content = self.linkedin_writer.write_post(query)
            elif agent_type == "image":
                content = self.image_generator.generate_image(query)
            else:
                content = {"error": "Unknown agent type"}
            
            state["content"] = content
            state["messages"].append(f"Content generated successfully")
        except Exception as e:
            state["error"] = str(e)
            state["messages"].append(f"Error: {str(e)}")
        
        return state
    
    def _should_continue(self, state: WorkflowState) -> str:
        """Determine if workflow should continue"""
        if state.get("error"):
            return "error"
        return "end"
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(WorkflowState)
        
        # Add nodes
        workflow.add_node("route", self._route_query)
        workflow.add_node("generate", self._generate_content)
        
        # Add edges
        workflow.set_entry_point("route")
        workflow.add_edge("route", "generate")
        workflow.add_conditional_edges(
            "generate",
            self._should_continue,
            {
                "end": END,
                "error": END
            }
        )
        
        return workflow.compile()
    
    def run(self, query: str) -> Dict[str, Any]:
        """Execute the workflow"""
        initial_state = {
            "query": query,
            "messages": [],
            "routing_info": {},
            "content": {},
            "error": ""
        }
        
        result = self.workflow.invoke(initial_state)
        return result

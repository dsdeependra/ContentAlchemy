"""
Streamlit web application for ContentAlchemy
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from src.workflow.langgraph_workflow import ContentAlchemyWorkflow
from src.core.config import Config


def format_metadata_value(value):
    """Format metadata value for display"""
    if isinstance(value, list):
        if len(value) == 0:
            return "None"
        return ", ".join(str(v) for v in value)
    elif isinstance(value, dict):
        return str(value)
    elif isinstance(value, bool):
        return "Yes" if value else "No"
    elif isinstance(value, (int, float)):
        return str(value)
    else:
        return str(value)


def main():
    st.set_page_config(
        page_title="ContentAlchemy",
        page_icon="✨",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            background: linear-gradient(45deg, #6366f1, #8e2de2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        .sub-header {
            color: #6b7280;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        .metadata-item {
            background-color: #f3f4f6;
            padding: 0.5rem;
            border-radius: 0.375rem;
            margin-bottom: 0.5rem;
        }
        .metadata-label {
            font-weight: 600;
            color: #374151;
        }
        .metadata-value {
            color: #6b7280;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-header">ContentAlchemy</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Content Marketing Assistant</div>', unsafe_allow_html=True)
    
    # Initialize workflow
    if 'workflow' not in st.session_state:
        config = Config()
        if not config.validate():
            st.error("⚠️ Please set OPENAI_API_KEY in your environment variables")
            st.info("Create a .env file with: OPENAI_API_KEY=your_key_here")
            st.stop()
        st.session_state.workflow = ContentAlchemyWorkflow(config)
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Sidebar
    with st.sidebar:
        
        st.header("📚 Quick Actions")
        example_prompts = {
            "🔍 Research Topic": "Research the latest trends in ",
            "📝 Write Blog": "Write a blog about ",
            "💼 LinkedIn Post": "Create a LinkedIn post about ",
            "🎨 Generate Image": "Generate an image for "
        }
        
        for label, prompt_start in example_prompts.items():
            if st.button(label):
                st.session_state.quick_prompt = prompt_start
        
        st.divider()
        
        st.header("ℹ️ Info")
        st.info("This app uses OpenAI GPT-4 and DALL-E 3 to generate content.")
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Chat Interface")
        
        # Display chat messages
        chat_container = st.container()
        with chat_container:
            if len(st.session_state.messages) == 0:
                st.info("👋 Welcome! Ask me to create any type of content - research reports, blog posts, LinkedIn posts, or images.")
            else:
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.write(message["content"])
                        if "data" in message and message["data"]:
                            with st.expander("📄 View Generated Content Details"):
                                content_data = message["data"]
                                st.json(content_data)
        
        # Chat input
        prompt = st.chat_input("Describe the content you want to create...")
        
        # Check for quick prompt
        if 'quick_prompt' in st.session_state and st.session_state.quick_prompt:
            prompt = st.session_state.quick_prompt
            st.session_state.quick_prompt = None
        
        if prompt:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Generate response
            with st.spinner("🤖 Generating content..."):
                try:
                    result = st.session_state.workflow.run(prompt)
                    
                    response_content = result.get("content", {})
                    
                    if response_content:
                        content_type = response_content.get('type', 'content')
                        # Add assistant message
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"✅ I've generated your {content_type}. Check the preview panel!",
                            "data": response_content
                        })
                    else:
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": "❌ Sorry, I couldn't generate content. Please try again.",
                            "data": None
                        })
                except Exception as e:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"❌ Error: {str(e)}",
                        "data": None
                    })
                
                st.rerun()
    
    with col2:
        st.subheader("👁️ Content Preview")
        
        if st.session_state.messages:
            # Find the last message with data
            last_content_data = None
            for message in reversed(st.session_state.messages):
                if "data" in message and message["data"]:
                    last_content_data = message["data"]
                    break
            
            if last_content_data:
                content_data = last_content_data
                
                # Display content type
                content_type = content_data.get("type", "unknown")
                st.info(f"📌 Type: {content_type.capitalize()}")
                
                # Display metadata in a nice format
                metadata_keys = ["word_count", "read_time", "seo_score", "keywords", "hashtags", 
                                "character_count", "engagement_score", "ideal_length", "sources", 
                                "topic", "prompt", "original_request", "size"]
                
                metadata_found = False
                for key in metadata_keys:
                    if key in content_data:
                        metadata_found = True
                        break
                
                if metadata_found:
                    with st.expander("📊 Metadata", expanded=True):
                        for key in metadata_keys:
                            if key in content_data:
                                value = content_data[key]
                                formatted_value = format_metadata_value(value)
                                
                                # Create a nice display for each metadata item
                                st.markdown(f"""
                                <div class="metadata-item">
                                    <span class="metadata-label">{key.replace('_', ' ').title()}:</span>
                                    <span class="metadata-value">{formatted_value}</span>
                                </div>
                                """, unsafe_allow_html=True)
                
                # Display content
                if "content" in content_data and content_data["content"]:
                    st.markdown("### 📄 Generated Content")
                    
                    content_text = content_data["content"]
                    
                    # Display in a text area for easy copying
                    st.text_area(
                        "Content", 
                        content_text, 
                        height=400,
                        label_visibility="collapsed"
                    )
                    
                    # Download buttons
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.download_button(
                            label="⬇️ Download TXT",
                            data=content_text,
                            file_name=f"{content_type}_content.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with col_b:
                        st.download_button(
                            label="⬇️ Download MD",
                            data=content_text,
                            file_name=f"{content_type}_content.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                
                # Display image if present
                if "image_url" in content_data and content_data["image_url"]:
                    st.markdown("### 🎨 Generated Image")
                    st.image(content_data["image_url"], caption="Generated Image", use_column_width=True)
                    
                    if "prompt" in content_data:
                        st.caption(f"**Optimized Prompt:** {content_data['prompt']}")
                
            else:
                st.info("💡 No content generated yet. Start a conversation to see your content here!")
        else:
            # Empty state
            st.markdown("""
                <div style="text-align: center; padding: 2rem; color: #6b7280;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📝</div>
                    <h3>No content yet</h3>
                    <p>Start by asking me to create content!</p>
                    <br>
                    <p><strong>Try these:</strong></p>
                    <ul style="list-style: none; padding: 0;">
                        <li>📊 "Research AI trends in 2024"</li>
                        <li>✍️ "Write a blog about productivity"</li>
                        <li>💼 "Create a LinkedIn post about leadership"</li>
                        <li>🎨 "Generate an image for a tech startup"</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
    
    # Footer with agent status
    st.divider()
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.caption("🤖 Multi-Agent System Powered by LangGraph | Built with Streamlit")
        with col2:
            if st.session_state.messages:
                st.caption(f"💬 {len(st.session_state.messages)} messages")


if __name__ == "__main__":
    main()
"""
Streamlit web application for ContentAlchemy
"""
import streamlit as st
from src.workflow.langgraph_workflow import ContentAlchemyWorkflow
from src.core.config import Config


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
            st.stop()
        st.session_state.workflow = ContentAlchemyWorkflow(config)
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Agent Status")
        agents = ["Query Handler", "Research", "Blog Writer", "LinkedIn Writer", "Image Generator", "Strategist"]
        for agent in agents:
            st.success(f"✓ {agent}")
        
        st.divider()
        
        st.header("📚 Quick Actions")
        if st.button("🔍 Research Topic"):
            st.session_state.quick_prompt = "Research the latest trends in "
        if st.button("📝 Write Blog"):
            st.session_state.quick_prompt = "Write a blog about "
        if st.button("💼 LinkedIn Post"):
            st.session_state.quick_prompt = "Create a LinkedIn post about "
        if st.button("🎨 Generate Image"):
            st.session_state.quick_prompt = "Generate an image for "
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Chat Interface")
        
        # Display chat messages
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
                    if "data" in message:
                        with st.expander("📄 View Generated Content"):
                            st.json(message["data"])
        
        # Chat input
        prompt = st.chat_input("Describe the content you want to create...")
        
        if prompt:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Generate response
            with st.spinner("🤖 Generating content..."):
                result = st.session_state.workflow.run(prompt)
                
                response_content = result.get("content", {})
                
                # Add assistant message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"I've generated your {response_content.get('type', 'content')}. Check the preview panel!",
                    "data": response_content
                })
                
                st.rerun()
    
    with col2:
        st.subheader("👁️ Content Preview")
        
        if st.session_state.messages:
            last_message = st.session_state.messages[-1]
            if "data" in last_message:
                content_data = last_message["data"]
                
                # Display content type
                content_type = content_data.get("type", "unknown")
                st.info(f"📌 Type: {content_type.capitalize()}")
                
                # Display metadata
                if "metadata" in content_data or any(k in content_data for k in ["word_count", "seo_score", "hashtags"]):
                    with st.expander("📊 Metadata", expanded=True):
                        for key, value in content_data.items():
                            if key not in ["content", "type", "image_url"]:
                                st.metric(key.replace("_", " ").title(), value)
                
                # Display content
                if "content" in content_data:
                    st.text_area("Generated Content", content_data["content"], height=400)
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download Content",
                        data=content_data["content"],
                        file_name=f"{content_type}_content.txt",
                        mime="text/plain"
                    )
                
                if "image_url" in content_data:
                    st.image(content_data["image_url"], caption="Generated Image")
        else:
            st.info("No content generated yet. Start a conversation!")


if __name__ == "__main__":
    main()

# ContentAlchemy - AI Content Marketing Assistant

<div align="center">

![ContentAlchemy Logo](https://via.placeholder.com/150)

**Transform your content marketing with AI-powered multi-agent system**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.0-green.svg)](https://langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.39.0-red.svg)](https://streamlit.io/)

</div>

---

## 🌟 Features

- 🤖 **6 Specialized AI Agents** - Each optimized for specific content types
- 🔍 **Deep Web Research** - Comprehensive research with source attribution
- 📝 **SEO-Optimized Blogs** - 1500+ word articles with keyword optimization
- 💼 **LinkedIn Posts** - Engaging professional content with hashtags
- 🎨 **AI Image Generation** - Custom visuals with DALL-E 3
- 🧠 **Intelligent Routing** - Automatic query-to-agent matching
- 💬 **Multi-Turn Conversations** - Context-aware interactions
- 📊 **Quality Metrics** - SEO scores, engagement predictions, readability

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- OpenAI API Key
- (Optional) SERP API Key for web research

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/contentalchemy.git
cd contentalchemy
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Run the application**
```bash
streamlit run src/web_app/streamlit_app.py
```

6. **Open in browser**
```
http://localhost:8501
```

---

## 📖 Usage Examples

### Research Content
```
"Research the latest AI trends in content marketing"
```

### Generate Blog Post
```
"Write a comprehensive blog about remote work productivity tips"
```

### Create LinkedIn Post
```
"Create an engaging LinkedIn post about leadership in tech"
```

### Generate Image
```
"Generate a modern professional image for a tech startup presentation"
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│         User Interface (Streamlit)          │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│         Query Handler Agent                 │
│         (LangGraph Orchestration)           │
└───┬─────────┬─────────┬─────────┬──────────┘
    │         │         │         │
    ▼         ▼         ▼         ▼
┌────────┐ ┌──────┐ ┌──────┐ ┌──────┐
│Research│ │ Blog │ │LinkedIn│Image │
│ Agent  │ │Writer│ │Writer │ Gen  │
└────────┘ └──────┘ └────────┘└──────┘
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Framework** | LangGraph 0.2.0 |
| **LLM** | OpenAI GPT-4 |
| **Research** | SERP API |
| **Images** | DALL-E 3 |
| **Interface** | Streamlit 1.39.0 |
| **Language** | Python 3.11+ |

---

## 📁 Project Structure

```
contentalchemy/
├── src/
│   ├── agents/              # All AI agents
│   │   ├── query_handler.py
│   │   ├── research_agent.py
│   │   ├── blog_writer.py
│   │   ├── linkedin_writer.py
│   │   ├── image_generator.py
│   │   └── content_strategist.py
│   ├── core/                # Core functionality
│   │   ├── config.py
│   │   └── router.py
│   ├── workflow/            # LangGraph workflows
│   │   └── langgraph_workflow.py
│   ├── web_app/             # Streamlit interface
│   │   └── streamlit_app.py
│   └── utils/               # Utilities
│       ├── content_optimization.py
│       └── quality_validation.py
├── tests/                   # Test suite
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── config/                  # Configuration files
├── docs/                    # Documentation
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## 🧪 Testing

Run the test suite:

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# With coverage
pytest --cov=src --cov-report=html
```

---

## 🐳 Docker Deployment

### Build and Run
```bash
docker build -t contentalchemy:latest .
docker run -p 8501:8501 -e OPENAI_API_KEY=your_key contentalchemy:latest
```

### Using Docker Compose
```bash
docker-compose up -d
```

---

## 📊 Performance Metrics

| Operation | Avg Time | Token Usage | Cost (GPT-4) |
|-----------|----------|-------------|--------------|
| Research | 8-12s | ~1200 | $0.024 |
| Blog Post | 15-20s | ~2000 | $0.040 |
| LinkedIn Post | 5-8s | ~500 | $0.010 |
| Image | 10-15s | ~300 | $0.040 |

---

## 🔐 Security

- 🔒 API keys stored in environment variables
- 🛡️ Input validation and sanitization
- 🔑 No data storage on servers
- 📝 Comprehensive logging for auditing

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md).

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the amazing framework
- [OpenAI](https://openai.com/) for GPT-4 and DALL-E
- [Streamlit](https://streamlit.io/) for the web framework
- The open-source community

---

## 📞 Support

- 📧 Email: support@contentalchemy.ai
- 💬 Discord: [Join our community](https://discord.gg/contentalchemy)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/contentalchemy/issues)
- 📖 Documentation: [Full Docs](https://docs.contentalchemy.ai)

---

## 🗺️ Roadmap

### Phase 1 - Current ✅
- [x] Multi-agent system
- [x] Basic content generation
- [x] Streamlit interface
- [x] Docker support

### Phase 2 - Q1 2024 🔄
- [ ] Video script generation
- [ ] Podcast content creation
- [ ] Multi-language support
- [ ] Advanced analytics

### Phase 3 - Q2 2024 📅
- [ ] CMS integration (WordPress, Ghost)
- [ ] Social media scheduling
- [ ] Custom model fine-tuning
- [ ] Mobile app

---

<div align="center">

**Made with ❤️ by the ContentAlchemy Team**

[Website](https://contentalchemy.ai) • [Documentation](https://docs.contentalchemy.ai) • [Blog](https://blog.contentalchemy.ai)

</div>

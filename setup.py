from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="contentalchemy",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered content marketing assistant with multi-agent system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/contentalchemy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    install_requires=[
        "langchain>=0.3.0",
        "langchain-openai>=0.2.0",
        "langchain-core>=0.3.0",
        "langgraph>=0.2.0",
        "streamlit>=1.39.0",
        "requests>=2.32.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.9.0",
    ],
)

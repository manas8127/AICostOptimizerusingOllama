AI Cost Optimization Advisor

This project is a Streamlit-based AI assistant that helps organizations optimize business costs using advanced Retrieval-Augmented Generation (RAG). It leverages a combination of document understanding, intelligent semantic retrieval, Lyzr agentic recommendations, and local Large Language Models (LLMs).

Features
Interactive Questionnaire: Collects detailed information about your company, workflows, technology stack, costs, workforce, customer engagement, goals, risks, and more.

RAG Pipeline: Extracts relevant answers from internal documentation (e.g., your own Tasks.pdf, manuals, or cost reports) using semantic search and reranking.

State-of-the-art Reranking: Uses Hugging Face’s BAAI/bge-reranker-v2-m3 model for precise, context-aware selection of information snippets prior to answer generation.

Local LLM-Powered Recommendations: Uses Ollama-hosted LLMs (e.g., Llama3) to generate actionable, tailored cost optimization strategies based specifically on your input and retrieved business context.

Lyzr Agentic Tools: The AI recommendations focus exclusively on Lyzr’s agentic automation tools, tailored to your use case.

Extensible & Private: All components run locally (your data/documentation never leaves your environment).

How It Works

User Input: Fill in company and process details through an easy Streamlit form.

Document Extraction: The app reads and chunks relevant internal documents (e.g., operations or task descriptions in PDF format).

Semantic Search: Chunks are matched against your input using embeddings and vector search.

Reranking: The top candidates are scored using a highly accurate cross-encoder reranking model to maximize retrieval relevance.

LLM Generation: The best-matching context is sent to a powerful local LLM for response generation, always focused on suggesting Lyzr-driven cost optimization.

Actionable Output: The insights and recommendations are visually returned in the app.

-> $pip install streamlit sentence-transformers transformers torch chromadb PyPDF2 ollama

Make sure Ollama is running and the model is installed

streamlit run streamlit.py



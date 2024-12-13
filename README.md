<div align="center">

# AI RAG Chain System

[English](README.md) | [繁體中文](README.zh-TW.md)

A RAG (Retrieval-Augmented Generation) system combining multiple AI models, supporting Gemini and Azure OpenAI services.

</div>

## Features

- Support for multiple AI models:
  - Google Gemini 1.0 Pro
  - Google Gemini 1.5 Pro
  - Azure OpenAI
- Vector Database Integration (FAISS)
- Chatbot Functionality
- CSV Data Loading and Vectorization
- RDF Graph Data Processing

## System Requirements

- Python 3.8+
- FastAPI
- LangChain
- FAISS
- Other dependencies (see requirements.txt)

## Environment Setup

1. Create a `.env` file and set the following environment variables:

```
GOOGLE_API_KEY=your_google_api_key
AZURE_OPENAI_DEPLOYMENT=your_azure_deployment
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=your_azure_embedding_deployment
AZURE_OPENAI_VERSION=your_azure_api_version
```

## Usage

### Start the Server

```bash
python server.py
```

The server will start at http://localhost:8000, providing the following endpoints:

- `/`: Gemini 1.0 Pro
- `/gemini_1.5`: Gemini 1.5 Pro
- `/azureopenai`: Azure OpenAI
- `/azureopenai/chat`: Azure OpenAI Chatbot

### Create Vector Index

```bash
python save_all_faiss.py
```

### Using the Client

```python
from langserve import RemoteRunnable
llama2 = RemoteRunnable("http://localhost:8000/azureopenai/")
response = llama2.invoke({"input": "your question"})
```

## Project Structure

```
.
├── server.py                    # Main server
├── gemini/                      # Gemini-related modules
│   ├── rag_chain.py
│   └── save_csv_to_faiss.py
├── azure_open_ai/              # Azure OpenAI-related modules
│   ├── chat_bot.py
│   ├── graph_chain.py
│   ├── rag_chain.py
│   └── save_csv_to_faiss.py
└── faiss/                      # FAISS vector index storage directory
```

## Important Notes

- Ensure all necessary API keys are properly configured before use
- Vector index creation may take time depending on data volume
- Implement appropriate security measures in production environments

## License

MIT License

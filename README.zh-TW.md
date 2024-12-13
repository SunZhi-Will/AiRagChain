<div align="center">

# AI RAG Chain 系統

[English](README.md) | [繁體中文](README.zh-TW.md)

這是一個結合多個AI模型的RAG（Retrieval-Augmented Generation）系統，支援Gemini和Azure OpenAI服務。

</div>

## 功能特點

- 支援多種AI模型：
  - Google Gemini 1.0 Pro
  - Google Gemini 1.5 Pro
  - Azure OpenAI
- 向量資料庫整合（FAISS）
- 聊天機器人功能
- CSV資料載入和向量化
- RDF圖形資料處理

## 系統需求

- Python 3.8+
- FastAPI
- LangChain
- FAISS
- 其他相依套件（見 requirements.txt）

## 環境設定

1. 建立 `.env` 檔案並設定以下環境變數：

```
GOOGLE_API_KEY=your_google_api_key
AZURE_OPENAI_DEPLOYMENT=your_azure_deployment
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=your_azure_embedding_deployment
AZURE_OPENAI_VERSION=your_azure_api_version
```

## 使用方式

### 啟動服務器

```bash
python server.py
```

服務器將在 http://localhost:8000 啟動，提供以下端點：

- `/`: Gemini 1.0 Pro
- `/gemini_1.5`: Gemini 1.5 Pro
- `/azureopenai`: Azure OpenAI
- `/azureopenai/chat`: Azure OpenAI 聊天機器人

### 建立向量索引

```bash
python save_all_faiss.py
```

### 使用客戶端

```python
from langserve import RemoteRunnable
llama2 = RemoteRunnable("http://localhost:8000/azureopenai/")
response = llama2.invoke({"input": "你的問題"})
```

## 專案結構

.
├── server.py # 主服務器
├── gemini/ # Gemini 相關模組
│ ├── rag_chain.py
│ └── save_csv_to_faiss.py
├── azure_open_ai/ # Azure OpenAI 相關模組
│ ├── chat_bot.py
│ ├── graph_chain.py
│ ├── rag_chain.py
│ └── save_csv_to_faiss.py
└── faiss/ # FAISS 向量索引儲存目錄


## 注意事項

- 使用前請確保已正確設定所有必要的API金鑰
- 向量索引建立可能需要一些時間，視資料量而定
- 建議在生產環境中使用適當的安全措施

## 授權

MIT License

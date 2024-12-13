from fastapi import FastAPI
from langserve import add_routes
from gemini.rag_chain import get_chain as gemini_chain
from azure_open_ai.rag_chain import get_chain as azure_open_ai_chain
from azure_open_ai.chat_bot import get_chain as azure_open_ai_chat_bot

app = FastAPI()


# Add the LangServe routes to the FastAPI app
add_routes(app, gemini_chain("./faiss/gemini_faiss_index"))
add_routes(app, gemini_chain("./faiss/gemini_faiss_index", True), path="/gemini_1.5")
add_routes(app, azure_open_ai_chain("./faiss/azure_faiss_index"), path="/azureopenai")
add_routes(app, azure_open_ai_chat_bot(), path="/azureopenai/chat")

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI app
    uvicorn.run(app, host="localhost", port=8000)



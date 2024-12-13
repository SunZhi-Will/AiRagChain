import os
from typing import List, Union

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.pydantic_v1 import BaseModel

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain.memory import ChatMessageHistory
from langchain.memory import VectorStoreRetrieverMemory
from langchain.chains import ConversationChain

# https://ithelp.ithome.com.tw/articles/10331266

load_dotenv()

# Create an AzureOpenAIEmbeddings model
embeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
    openai_api_version=os.getenv("AZURE_OPENAI_VERSION"),
)
# Create a ChatOpenAI model
llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"), 
    openai_api_version=os.getenv("AZURE_OPENAI_VERSION"),
    temperature=0
)

db_chroma = FAISS.from_texts(["foo"], embeddings)

retriever = db_chroma.as_retriever(search_kwargs=dict(k=4))

memory_vs = VectorStoreRetrieverMemory(retriever=retriever, return_messages=True)


def get_chain():
    _DEFAULT_TEMPLATE = """
    你是一個友善的對話機器人，下面歷史記錄是我們曾經的對話。
    Human 是我，AI 是你。請根據歷史記錄中的資訊來回覆我的新問題。

    歷史記錄:
    {history}

    Human：{input}
    AI：
    """
    prompt = PromptTemplate(
        input_variables=["history", "input"], template=_DEFAULT_TEMPLATE
    )
    rag_chain = ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=memory_vs,
        verbose=True,
        output_key='AI'
    )

    # Add typing for input
    class Question(BaseModel):
        __root__: str

    full_chain = rag_chain.with_types(input_type=Question)
    return full_chain
import os
from typing import List, Union

from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import AzureChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.pydantic_v1 import BaseModel

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser

db = SQLDatabase.from_uri("sqlite:///data.db")
# print(db.dialect)
# print(db.get_usable_table_names())

load_dotenv()


embeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
    openai_api_version=os.getenv("AZURE_OPENAI_VERSION"),
)
# Create a ChatOpenAI model
llm_text = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"), 
    openai_api_version=os.getenv("AZURE_OPENAI_VERSION"),
    temperature=0
)

def get_chain(faiss_path):
    vectorstore = FAISS.load_local(
        faiss_path, embeddings, allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever()

    template = """
    Answer given the following context:
    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)


    # Add typing for input
    class Question(BaseModel):
        __root__: str
    class InputChat(BaseModel):
        input: str


    # SQL 資料
    # agent_executor  = create_sql_agent(llm_text, db=db, agent_type="openai-tools", verbose=True)
    
    # validation_chain = prompt | llm_text | StrOutputParser()

    # rag_chain = {
    #     "context": agent_executor,
    #     "question": RunnablePassthrough()
    #     } | validation_chain
    

    rag_chain = (
        {
        "context": retriever,
        "question": RunnablePassthrough()
        }
        | prompt
        | llm_text
        | StrOutputParser()
    )


    full_chain = rag_chain.with_types(input_type=Question)
    return full_chain
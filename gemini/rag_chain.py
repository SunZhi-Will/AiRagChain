# pip install --upgrade  langchain langchain-google-genai "langchain[docarray]" faiss-cpu

import os
import getpass
import requests
from PIL import Image
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.pydantic_v1 import BaseModel

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from IPython.display import display, Markdown

from langchain_community.vectorstores import FAISS

import matplotlib.pyplot as plt

from operator import itemgetter

from langchain_community.document_loaders import UnstructuredExcelLoader
from dotenv import load_dotenv


load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
llm_text = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
llm_text_10 = ChatGoogleGenerativeAI(model="gemini-1.0-pro", temperature=0)

def get_chain(faiss_path, is_gemini_1_5 = False):
    vectorstore = FAISS.load_local(
        faiss_path, embeddings, allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever()

    template = """
    查詢資料:
    {context}

    問題: {question}

    依照查詢資料回答問題
    """
    prompt = ChatPromptTemplate.from_template(template)


    # Add typing for input
    class Question(BaseModel):
        __root__: str
    
    
    if is_gemini_1_5: 
        llm =llm_text 
    else: 
        llm =llm_text_10

    rag_chain = (
        {
        "context": retriever,
        "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )


    full_chain = rag_chain.with_types(input_type=Question)
    return full_chain


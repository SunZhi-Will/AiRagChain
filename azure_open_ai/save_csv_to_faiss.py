import os

from langchain_openai import AzureOpenAIEmbeddings

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from IPython.display import display, Markdown
from langchain_community.vectorstores import FAISS
import matplotlib.pyplot as plt
from operator import itemgetter
from langchain.document_loaders.csv_loader import CSVLoader
from dotenv import load_dotenv


load_dotenv()

# 載入 Azure OpenAI Embeddings
embeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
    openai_api_version=os.getenv("AZURE_OPENAI_VERSION"),
)

# 載入資料
def save_faiss_index(data_path, output_path):
    # 載入資料
    print("載入資料")
    loader = CSVLoader(data_path)
    docs = loader.load()

    # 建立 FAISS 索引
    print("建立 FAISS 索引")
    db = FAISS.from_documents(
        docs, embedding=embeddings
    )

    # 儲存 FAISS 索引
    print("儲存 FAISS 索引")
    db.save_local(output_path)

    return db

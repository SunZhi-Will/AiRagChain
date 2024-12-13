import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from IPython.display import display, Markdown
from langchain_community.vectorstores import FAISS
import matplotlib.pyplot as plt
from operator import itemgetter
from langchain.document_loaders.csv_loader import CSVLoader

if "GOOGLE_API_KEY" not in os.environ:
    from dotenv import load_dotenv
    import os
    # 加载.env文件中的环境变量
    load_dotenv()
    GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


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

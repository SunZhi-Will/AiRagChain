import requests
from bs4 import BeautifulSoup
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef

# 定義你想要抓取的網頁 URL
url = "https://www.w3.org/People/Berners-Lee/"

# 使用 requests 庫抓取網頁
response = requests.get(url)

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(response.text, 'html.parser')

# 建立一個 RDF 圖
g = Graph()

# 定義一個命名空間
n = Namespace("https://www.w3.org/People/Berners-Lee/")

# 遍歷 HTML 中的所有元素
for tag in soup.find_all(True):
    # 為每個元素創建一個節點
    node = BNode()
    
    # 將節點添加到圖中
    g.add((node, RDF.type, URIRef(f"http://www.w3.org/1999/xhtml#{tag.name}")))
    
    # 如果元素有內容，則將其添加到圖中
    if tag.string:
        g.add((node, n.content, Literal(tag.string)))

# 將 RDF 圖序列化並儲存到檔案中
g.serialize(destination='test.ttl', format='turtle')
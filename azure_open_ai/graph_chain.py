import os
from dotenv import load_dotenv
from langchain.chains import GraphSparqlQAChain
from langchain_community.graphs import RdfGraph
from langchain_openai import AzureChatOpenAI, ChatOpenAI

load_dotenv()


graph = RdfGraph(
    source_file="test.ttl",
    standard="rdf",
    local_copy="test.ttl",
)

llm_text = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"), 
    openai_api_version=os.getenv("AZURE_OPENAI_VERSION"),
    temperature=0
)

chain = GraphSparqlQAChain.from_llm(
    llm_text, graph=graph, verbose=True
)
text = "(When generating SPARQL queries, omit the use of triple backticks to avoid formatting the query as a code block.)"

graph.load_schema()
print(graph.get_schema)
print(chain.run(text + 
    "Save that the person with the name 'Timothy Berners-Lee' has a work homepage at 'http://www.w3.org/foo/bar/'"
))
graph.load_schema()
print(graph.get_schema)
print(chain.run(text + "What is Timothy Berners-Lee work homepage?"))
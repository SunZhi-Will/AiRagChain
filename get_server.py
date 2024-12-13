from langserve import RemoteRunnable
llama2 = RemoteRunnable("http://localhost:8000/azureopenai/")
response = llama2.invoke({"input": "Describe the playlisttrack table"})
print(response)
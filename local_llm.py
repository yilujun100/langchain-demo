# 使用本地大模型
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model='qwen3:1.7b',
    base_url='http://localhost:11434'  # LangChain 会通过此地址访问容器
)
message = llm.invoke('讲一个笑话')
print(message)

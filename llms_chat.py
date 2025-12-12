from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import OllamaLLM, ChatOllama

# 1. LLMs: 一问一答，输入和返回都是纯文本，适合做一些简单的与大模型交互的功能
# llm = OllamaLLM(model='qwen3:1.7b')
# response = llm.invoke('你是谁?')
# print(response)

# 2. ChatModel: 支持多轮对话、支持结构化输出、支持多模态输入和输出
llm = ChatOllama(model='qwen3:1.7b')
messages = [
    SystemMessage('你是一个资深 Python 开发工程师'),
    HumanMessage('请帮我写一个冒泡排序')
]
# 返回的是 AIMessage
response = llm.invoke(messages)
print(response)

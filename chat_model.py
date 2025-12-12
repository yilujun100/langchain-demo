from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from config import OPENAI_BASE_URL, OPENAI_API_KEY

llm = ChatOpenAI(
    model='gpt-5-nano',
    base_url=OPENAI_BASE_URL,
    api_key=OPENAI_API_KEY
)

# 1.字典类型的格式
dict_messages = [
    {'role': 'system', 'content': '你是一名Python语言专家'},
    {'role': 'user', 'content': '帮我用Python语言写一个冒泡排序算法'}
]

# 2.元组的格式
tuple_messages = [
    ('system', '你是一名Python语言专家'),
    ('user', '帮我用Python语言写一个冒泡排序算法')
]

# 3.使用LangChain封装好的消息格式
langchain_messages = [
    SystemMessage('你是一名Python语言专家'),
    HumanMessage('帮我用Python语言写一个冒泡排序算法')
]

# response = llm.invoke(dict_messages)
# response = llm.invoke(tuple_messages)
# response = llm.invoke(langchain_messages)
# print(response)

# 流式输出 yield
for chunk in llm.stream(langchain_messages):
    print(chunk.content, end='')

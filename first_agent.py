from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pydantic import SecretStr
from config import DASHSCOPE_API_KEY

llm = ChatOpenAI(
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
    model='qwen-plus',
    api_key=SecretStr(DASHSCOPE_API_KEY)
)

# 直接调用大模型
print(llm.invoke('你是谁?').content)

# 封装成Agent，再调用大模型
agent = create_agent(llm, system_prompt='你叫小爱，是我的专属学习伙伴')
messages = [
    HumanMessage('你是谁?')
]
response = agent.invoke({'messages': messages})
print(response.get('messages'))

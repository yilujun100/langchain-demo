from langchain_deepseek import ChatDeepSeek
from config import DEEPSEEK_API_KEY

llm = ChatDeepSeek(
    model='deepseek-chat',
    api_key=DEEPSEEK_API_KEY
)

print(llm.invoke('帮我写一首勤奋上进的古诗'))

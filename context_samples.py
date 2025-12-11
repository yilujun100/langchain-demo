from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from sqlalchemy import create_engine

from config import OPENAI_BASE_URL, OPENAI_API_KEY

llm_openai = ChatOpenAI(
    base_url=OPENAI_BASE_URL,
    api_key=OPENAI_API_KEY,
    model='gpt-5-nano',
    temperature=1.0
)

parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ('system', '你是一个幽默的聊天机器人'),
    MessagesPlaceholder(variable_name='history'),
    ('human', '{input}')
])

# LCEL 表达式
chain = prompt | llm_openai | parser

# 把聊天记录保存到本地数据库中
# 创建 SQLite 连接
engine = create_engine('sqlite:///chat.db')


def get_session_history(sid):
    return SQLChatMessageHistory(sid, connection=engine)


runnable = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key='input',
    history_messages_key='history'
)

# 调用
res1 = runnable.invoke({'input': '中国一共有哪些直辖市?'}, config={'configurable': {'session_id': 'ylj001'}})
print(res1)
print('--' * 30)
res2 = runnable.invoke({'input': '这些城市中，哪个最大?'}, config={'configurable': {'session_id': 'ylj001'}})
print(res2)

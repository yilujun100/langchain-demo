from typing import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from pydantic import SecretStr
from typing_extensions import NotRequired
from config import DASHSCOPE_API_KEY
import uuid

llm = ChatOpenAI(
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
    model='qwen-plus',
    api_key=SecretStr(DASHSCOPE_API_KEY)
)


class State(TypedDict):
    author: NotRequired[str]
    joke: NotRequired[str]


def author_node(state: State):
    prompt = '帮我推荐一位受人们欢迎的作家。只需要给出作家的名字即可。'
    author = llm.invoke(prompt)
    return {'author': author.content}


def joke_node(state: State):
    prompt = f'用作家: {state['author']} 的风格，写一个100字以内的笑话'
    joke = llm.invoke(prompt)
    return {'joke': joke.content}


# 构建工作流
workflow = StateGraph(State)
# 添加节点
workflow.add_node(author_node)
workflow.add_node(joke_node)
# 添加边来连接节点
workflow.add_edge(START, 'author_node')
workflow.add_edge('author_node', 'joke_node')
workflow.add_edge('joke_node', END)

checkpointer = InMemorySaver()
chain = workflow.compile(checkpointer=checkpointer)
print(chain.get_graph().draw_ascii())

# 正常执行一个图
config = {
    'configurable': {
        'thread_id': uuid.uuid4()
    }
}
state = chain.invoke({}, config)
print('Initial joke: ', state)

# 查看所有checkpoint检查点
states = list(chain.get_state_history(config))
# 推荐作家那一步
selected_state = states[1]
# 重新设定State
new_config = chain.update_state(selected_state.config, values={'author': '郭德纲'})
# 重新执行Graph
new_state = chain.invoke(None, new_config)
print('Improved joke: ', new_state)

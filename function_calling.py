from langchain_core.messages import AIMessage
from langchain_deepseek import ChatDeepSeek
from langchain_core.tools import tool
from config import DEEPSEEK_API_KEY

llm = ChatDeepSeek(
    model='deepseek-chat',
    api_key=DEEPSEEK_API_KEY
)


@tool
def add_tool(a: int, b: int) -> int:
    """
    计算两数相加的工具
    :param a: 第一个加数
    :param b: 第二个加数
    :return: 两数相加后的结果
    """
    return a + b


@tool
def sub_tool(a: int, b: int) -> int:
    """
    计算两数相减的工具
    :param a: 被减数
    :param b: 减数
    :return: 两数相减后的结果
    """
    return a - b


tools = {
    add_tool.name: add_tool,
    sub_tool.name: sub_tool
}

llm_with_tools = llm.bind_tools(tools=list(tools.values()))
message: AIMessage = llm_with_tools.invoke('帮我计算2加3等于多少？')
print(message)
# 如果返回值有tool_calls,说明选择了工具
if message.tool_calls:
    for tool_call in message.tool_calls:
        tool_name = tool_call.get('name')
        tool_args = tool_call.get('args')
        tool = tools.get(tool_name)
        res = tool.invoke(tool_args)
        print(f'工具执行后的结果: {res}')
# 注意：大模型选择完工具后，需要手动执行得到结果

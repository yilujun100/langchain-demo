from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage, AIMessage
from langchain_core.tools import tool

from config import DEEPSEEK_API_KEY

llm = ChatDeepSeek(
    model='deepseek-chat',
    api_key=DEEPSEEK_API_KEY
)


@tool
def get_weather():
    """
    获取今天的天气情况
    :return: 今天的天气信息
    """
    return (
        '天气: 晴天',
        '温度: 24~30摄氏度',
        '风量: 微风',
        '湿度: 91.1%'
    )


tools = {
    get_weather.name: get_weather
}
# 初始消息历史
messages = [
    SystemMessage('你是一个非常贴心的私人助手！'),
    HumanMessage('帮我查看一下今天的天气如何，如果下雨，我就不出去了。请问我今天可以出去玩吗？')
]
# 1.绑定工具
llm_with_tools = llm.bind_tools(tools=list(tools.values()))
# 2.第一次调用：模型决定是否调用工具
message: AIMessage = llm_with_tools.invoke(messages)
# 3.处理工具调用
if message.tool_calls:
    # 将模型的消息（包含 tool_calls）添加到历史记录
    messages.append(message)
    for tool_call in message.tool_calls:
        tool_call_id = tool_call.get('id')
        tool_call_name = tool_call.get('name')
        tool_call_args = tool_call.get('args')
        # 执行工具
        tool = tools.get(tool_call_name)
        res = tool.invoke(tool_call_args)
        print(f'{tool_call_name}执行后的结果为：{res}')
        # 4.构建 ToolMessage 并添加到历史记录
        messages.append(
            ToolMessage(
                content=res,
                tool_call_id=tool_call_id,
                artifact='可以随意携带的数据，这些数据不会发送给大模型'
            )
        )

final_message: AIMessage = llm_with_tools.invoke(messages)
print(final_message)

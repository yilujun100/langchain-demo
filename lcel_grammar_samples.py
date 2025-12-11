# LCEL 语法示例
import time

from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough
from langchain_core.tracers import Run

# 1. Runnable 节点
uppercase_node = RunnableLambda(lambda x: x.upper())
print(uppercase_node.invoke('hello'))

# 2.节点调用
# 普通调用
print(uppercase_node.invoke('langchain'))

# 批量调用
print(uppercase_node.batch(['a', 'b', 'c']))


# 流式输出
def stream_output(prompt: str):
    for char in prompt.split(' '):
        yield char


for chunk in RunnableLambda(stream_output).stream('What a wonderful picture!'):
    print(chunk)

# 3. 组合链，使用管道操作符 | 将 Runnable 节点组合成一个顺序执行的链 prompt | llm | parser
r1 = RunnableLambda(lambda x: x + 10)
r2 = RunnableLambda(lambda x: x * 2)
chain1 = r1 | r2  # 串行
print(chain1.invoke(2))

# 4.并行运行
chain = RunnableParallel(r1=r1, r2=r2)
print(chain.invoke(2, config={'max_concurrency': 3}))  # max_concurrency: 最大并发数

new_chain = chain1 | chain
new_chain.get_graph().print_ascii()  # 打印链的图像描述
print(new_chain.invoke(2))

# 5.合并输入、并处理中间数据
# RunnablePassthrough: 允许传递输入数据，可以保持不变或添加额外的键。
wrap_node = RunnableLambda(lambda x: {'text': x})
len_node = RunnableLambda(lambda x: len(x['text']))
chain = uppercase_node | wrap_node | RunnablePassthrough.assign(length=len_node)
print(chain.invoke('Hi'))


# 6.后备选项 with_fallbacks
def failing_func(input):
    raise ValueError('故意失败，模拟服务器宕机或API错误')


failing_runnable = RunnableLambda(failing_func)
fallback_runnable = RunnableLambda(lambda x: '使用备选方法回答：抱歉，服务暂时不可用。')
chain = failing_runnable.with_fallbacks([fallback_runnable])
print(chain.invoke(1))

# 7.节点失败，尝试再次运行 with_retry(容错)
count = 0


def unstable_func(input_data):
    global count
    count += 1

    # 第一次和第二次都抛出异常
    if count <= 2:
        print(f'[尝试 {count}]: 失败，抛出 ValueError')
        raise ValueError('模拟网络或 API 错误')
    # 第三次尝试成功
    print(f'[尝试 {count}]: 成功！')
    return f'成功处理后的数据: {input_data}'


unstable_runnable = RunnableLambda(unstable_func)
fault_tolerant_runnable = unstable_runnable.with_retry(
    stop_after_attempt=5
)

result = fault_tolerant_runnable.invoke('test input')
print(f'最终结果: {result}')
print(f'总共尝试次数: {count}')

# 8.根据条件动态的构建链
repeat_node = RunnableLambda(lambda x: x * 2)
chain = uppercase_node | RunnableLambda(lambda x: repeat_node if len(x) > 5 else RunnableLambda(lambda x: x))
# print(chain.invoke('hello langchain!'))
print(chain.invoke('hello'))


# 9.生命周期管理
def test(n: int):
    time.sleep(n)
    return n * 2


def on_start(run_obj: Run):
    # 节点启动时，自动调用
    print(f'节点启动时间: {run_obj.start_time}')


def on_end(run_obj: Run):
    # 节点运行结束时，自动调用
    print(f'节点结束时间: {run_obj.end_time}')


test_runnable = RunnableLambda(test)
chain = test_runnable.with_listeners(on_start=on_start, on_end=on_end)
print(chain.invoke(2))

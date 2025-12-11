from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from config import OPENAI_BASE_URL, OPENAI_API_KEY

llm = ChatOpenAI(
    model='gpt-5-nano',
    temperature=1.0,
    base_url=OPENAI_BASE_URL,
    api_key=OPENAI_API_KEY
)

# 提示词模板
# prompt = [
#     SystemMessage(
#         'You are a helpful assistant that translates English to Japanese. Translate the user sentence.'
#     ),
#     HumanMessage('How is the weather today?')
# ]

prompt = ChatPromptTemplate.from_messages(
    [
        ('system', 'You are a helpful assistant that can translate the user sentence into {language}.'),
        ('human', '{user_sentence}')
    ]
)

# 第一种
parser = StrOutputParser()
# response = llm.invoke(prompt)
# print('>>>', response)
# print('>>>content: ', parser.invoke(response))

# 第二种: LCEL
chain = prompt | llm | parser
res = chain.invoke({'language': 'Japanese', 'user_sentence': 'How is the weather today?'})
print('>>>res content: ', res)

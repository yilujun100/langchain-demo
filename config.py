from dotenv import load_dotenv
import os

load_dotenv(override=True)

OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')

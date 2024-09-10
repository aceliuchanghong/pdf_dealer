from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# 加载.env文件
load_dotenv()

llm = ChatOpenAI(
    model=os.getenv('MODEL'),
    api_key=os.getenv('API_KEY'),
    openai_api_base=os.getenv('BASE_URL')
)

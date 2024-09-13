import time

from openai import OpenAI
from dotenv import load_dotenv
import os

from z_utils.check_str2json import parse_json_markdown

system_prompt = """
基本信息:
"世界上最高的山是珠穆朗玛峰。"
用户将提供一些基本信息和问题输入,请根据基本信息解析"question"和"answer",并以JSON格式输出(不清楚回答:DK)
示例问题输入:
世界上最高的山是?
示例JSON输出:
{
    "question": "世界上最高的山是?",
    "answer": "珠穆朗玛峰"
}
"""
md_path = r'C:\Users\liuch\Documents\img20240708_16193473_latex.md'
with open(md_path, 'r', encoding='utf-8') as file:
    content = file.read()
Basic_info = "基本信息:\n" + content[1000:3000]+ "\n问题输入:\n"

load_dotenv()
client = OpenAI(api_key=os.getenv('API_KEY'), base_url=os.getenv('BASE_URL'))

if __name__ == '__main__':
    # user_prompt = "合同里面6块钱一个的电容销售了多少个?格式为纯数字"
    # user_prompt = '乙方传真号码是多少?'
    # user_prompt = '甲方传真号码是多少?'
    user_prompt = '电容 (G) CT41G-1206-X7R 50V-0.33 数量'
    # user_prompt = "合同里面SOB或者SOA编号是?格式是SOB..."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": Basic_info + user_prompt},
    ]
    start_time = time.time()  # 记录开始时间
    response = client.chat.completions.create(
        model="mistral-nemo:12b-instruct-2407-fp16",
        # model='reflection',
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.0
    )
    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算耗时
    print(f"回答耗时: {elapsed_time:.2f}秒\n")

    ans_temp = response.choices[0].message.content
    print(messages)
    print(parse_json_markdown(ans_temp))

import time
from dotenv import load_dotenv
import os
import logging
from z_utils.get_json import parse_json_markdown

load_dotenv()
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)


def get_entity_result(client, user_prompt, Basic_info=''):
    system_prompt = """
    示例基本信息:
    "世界上最高的山是珠穆朗玛峰。"
    示例问题输入:
    "世界上最高的山是?"
    用户将提供一些基本信息和问题输入,请根据基本信息解析"question"和"answer"
    1.以JSON格式输出
    2.没有满足其正则表达回答DK
    3.在提供的基本信息中找不到回答DK
    示例JSON输出:
    {
        "question": "世界上最高的山是?",
        "answer": "珠穆朗玛峰"
    }
    """
    prompt = ("基本信息:\n" + Basic_info if len(Basic_info) > 10 else "") + "\n问题输入:\n" + user_prompt
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    start_time = time.time()
    response = client.chat.completions.create(
        model=os.getenv('MODEL'),
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.1
    )
    end_time = time.time()
    elapsed_time = end_time - start_time
    ans_temp = response.choices[0].message.content

    logger.debug(f"大模型prompt: {prompt}")
    logger.debug(f"LLM回答耗时: {elapsed_time:.2f}秒")
    logger.debug(f"大模型response:{response}")
    return parse_json_markdown(ans_temp)


if __name__ == '__main__':
    from z_utils.get_model import TALK_LLM

    client = TALK_LLM()
    md_path = r'C:\Users\liuch\Documents\img20240708_16193473_latex.md'
    with open(md_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # user_prompt = "甲方传真号码是多少?"
    user_prompt = "合同里面SOB或者SOA编号是?"
    print(get_entity_result(client, user_prompt, content[:1000]))

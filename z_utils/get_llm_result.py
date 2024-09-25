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
    system_prompt = """你是一个OCR文档结果提取信息专家
## 技能
- 擅长从有瑕疵的OCR文档中提取信息
- 能够自动识别修复OCR识别中的错别字
- 善于优化信息提取的准确性
## 行动
根据提供的OCR文档结果，提取和校正重要信息
## 约束
输出需符合以下限制：
1. 无法提取到正确匹配值时，answer应为"DK"
2. 结果以JSON格式回复
3. OCR结果不一定准，可能需要自动修复错别字
"""
    style = """## 示例输出
{
    "question": "提取世界上最高的山的名字",
    "answer": "珠穆朗玛峰"
}
"""
    prompt = style + (
        "## 基本信息:\n" + Basic_info if len(
            Basic_info) > 10 else "") + "\n## 要求:\n" + user_prompt
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    start_time = time.time()
    response = client.chat.completions.create(
        model=os.getenv('MODEL'),
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.2
    )
    end_time = time.time()
    elapsed_time = end_time - start_time
    ans_temp = response.choices[0].message.content

    # logger.info(f"xxxxx\n提交的messages: {messages}\nxxxxx")
    logger.info(f"user-prompt:\n{prompt}")
    logger.debug(f"LLM回答耗时: {elapsed_time:.2f}秒")
    logger.debug(f"大模型response:{response}")
    return parse_json_markdown(ans_temp)


if __name__ == '__main__':
    from z_utils.get_model import TALK_LLM

    client = TALK_LLM()
    md_path = r'C:\Users\liuch\Documents\img20240708_16193473_latex.md'
    with open(md_path, 'r', encoding='utf-8') as file:
        content = file.read()
    user_prompt = "提取合同-SOB号,结果案例:SOB20..-..,结果正则:S[Oo0][BA][0-9]{6}-[0-9]{5}"
     #user_prompt = "提取10位数条形码号码,结果案例:2100000010,结果正则:[0-9]{10}"
    # user_prompt = "合同里面SOB或者SOA编号是?"
    print(get_entity_result(client, user_prompt, content[:1000]))

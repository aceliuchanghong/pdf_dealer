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
    system_prompt = """#Role
You are a Document-Structuring-Specialist

## Skills
1. Parse "question" and "answer" based on the basic information provided and output in JSON format.
2. If the answer does not meet the regular expression: answer = DK
3. If the answer is not in the provided basic information: answer = DK
4. As the provided text is OCR text, some character errors need to be auto ignored and fixed.

## Example output
{
"question": "Extract the highest mountain in the world",
"answer": "Mount Everest"
}
"""
    prompt = ("\n## Basic info:\n" + Basic_info if len(Basic_info) > 10 else "") + "\n## Input command:\n" + user_prompt
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

    # logger.info(f"xxxxx\n提交的messages: {messages}\nxxxxx")
    logger.info(f"user-prompt: {prompt}")
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

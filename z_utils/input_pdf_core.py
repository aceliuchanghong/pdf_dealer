import os
import sys
from pdf2image import convert_from_path
from dotenv import load_dotenv
from tqdm import tqdm
import logging
from z_utils.check_db import excute_sqlite_sql
from z_utils.get_llm_result import get_entity_result
from z_utils.get_model import TALK_LLM
from z_utils.get_ocr_result import get_latex_table, easy_ocr
from z_utils.get_text_chunk import chunk_by_LCEL
from z_utils.rotate2fix_pic import detect_text_orientation
from z_utils.sql_sentence import select_rule_sql

log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)),
            '../')))

load_dotenv()


def process_pdf(pdf_file_path):
    # apt install poppler-utils
    pdf2img_output_path = os.path.join(os.getenv('UPLOAD_FILE_PATH'), 'pdf2img_output_path',
                                       os.path.basename(pdf_file_path).split('.')[0])
    os.makedirs(pdf2img_output_path, exist_ok=True)
    images = convert_from_path(pdf_file_path)
    image_paths = []
    for i, image in enumerate(tqdm(images, desc="Converting PDF to PNG images")):
        image_path = os.path.join(pdf2img_output_path, f"page_{i + 1}.png")
        image.save(image_path, 'PNG')
        image_paths.append(image_path)
    return image_paths


def process_file(file_original):
    if file_original is None:
        return ['z_using_files/pics/ell-wide-dark.png'], []
    if file_original.endswith('.pdf'):
        cut_pics = process_pdf(file_original)
        return cut_pics, cut_pics
    else:
        return [file_original], [file_original]


def quick_ocr_image(image_list, quick_ocr):
    ocr_result_list = []
    ocr_type = 'format'
    for i, image in enumerate(image_list):
        try:
            rotate_image = detect_text_orientation(image, os.path.join(os.getenv('UPLOAD_FILE_PATH'), 'rotate_image'))
        except Exception as e:
            rotate_image = image
        if not quick_ocr:
            ans1 = easy_ocr(rotate_image)
            # ans2 = get_latex_table(rotate_image, ip=os.getenv('GOT_OCR_ip'), ocr_type='ocr')
            ans = get_latex_table(rotate_image, ip=os.getenv('GOT_OCR_ip'), ocr_type=ocr_type) + ans1
        else:
            ans = easy_ocr(rotate_image)
        logger.info(f"ocr ans: {ans}")
        ocr_result_list.append(ans)
    logger.debug(f"ocr_result_list: {ocr_result_list}")
    return ocr_result_list


def extract_short_entity(rule, ocr_result_list):
    text_all = ''.join(ans for ans in ocr_result_list)
    need_items = []
    tasks = []
    entity_tuple_list = excute_sqlite_sql(select_rule_sql, (rule,), False)
    for i, entity in enumerate(entity_tuple_list):
        task = {
            "entity_name": entity[0],
            "entity_format": entity[1],
            "entity_regex_pattern": entity[2],
            "entity_order": entity[3],
        }
        prompt_temp = "提取" + task["entity_name"] + \
                      (",其可能样例是:" + task["entity_format"] if len(task["entity_format"]) > 1 else "") + \
                      (",其可能的正则表达式为:" + task["entity_regex_pattern"] if len(
                          task["entity_regex_pattern"]) > 1 else "")
        need_items.append(prompt_temp)
        tasks.append(task)
    logger.info(f"need_items: {need_items}")

    entity_list = []
    client = TALK_LLM()

    for i, need_item in enumerate(need_items):
        entity = {}
        extracted_entity_name = tasks[i]["entity_name"]
        ans = get_entity_result(client, need_item, text_all)
        logger.info(f"llm ans_{i}: {ans}")

        entity['sure'] = False
        entity['rule_name'] = rule
        entity['entity_name'] = extracted_entity_name
        if 'answer' in ans and ans['answer'] != 'DK':
            entity['result'] = ans['answer']
        else:
            entity['result'] = 'DK'

        entity['remark'] = tasks[i]["entity_order"]
        entity_list.append(entity)
    return entity_list
    # return [
    #     {"sure": False, "rule_name": "提取合同信息规则", "entity_name": "条形码号码", "result": "210003526766"},
    #     {"sure": False, "rule_name": "提取合同信息规则", "entity_name": "合同-SOB号", "result": "SOB2015"},
    #     {"sure": False, "rule_name": "提取合同信息规则", "entity_name": "业务员姓名", "result": "张三3"},
    #     {"sure": False, "rule_name": "提取合同信息规则", "entity_name": "购买方公司名称", "result": "X7X有限公司"},
    # ]


if __name__ == '__main__':
    pdf_file_path = r'D:\wechatWork\WXWork\1688857567577400\Cache\File\2024-09\2024年中国AI大模型场景探索及产业应用调研报告.pdf'
    x, y = process_file(pdf_file_path)

import os
import time
import requests
import logging
import json
import re

from z_utils.get_latex_table import get_latex_table

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 匹配并替换图片
def replace_images(md_content, img_dict):
    def replacer(match):
        img_path = match.group(2)
        img_desc = match.group(1)
        if img_path in img_dict:
            replacement = img_dict[img_path]
            if img_desc:
                replacement = f"*{img_desc}:*\n{replacement}\n"
            return replacement
        return match.group(0)  # 如果图片不在字典中，保持原样

    pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
    return pattern.sub(replacer, md_content)


def parse_minerU_middle_json(middle_json_file_path):
    # 读取JSON文件,获取表格图片位置
    with open(middle_json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    table_image_list = []
    for page_info in data['pdf_info']:
        for page_block in page_info['preproc_blocks']:
            if page_block['type'] == 'table':
                for table_image in page_block['blocks']:
                    if table_image['type'] == 'table_body':
                        name = table_image['lines'][0]['spans'][0]['image_path']
                        table_image_list.append(name)
    logger.debug(f"所有的表格图片: {table_image_list}")
    return table_image_list


def pdf2md(file_ori_path, file_out_path, *, ocr_mode='auto'):
    url = f"http://{ip}:9521/convert-pdf/"
    data = {
        "input_pdf_path": file_ori_path,
        "output_dir": file_out_path,
        "mode": ocr_mode
    }
    start_time = time.time()
    response = requests.post(url, params=data)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"minerU转为md花费: {elapsed_time} s")

    if response.status_code == 200:
        logger.debug(f"Success:{response.json()}")
    else:
        logger.error(f"Error: status_code:{response.status_code}, response:{response.json()}")
    return response.json()


def get_latex_table_md(md_file_path, images_list):
    result = {}
    for i, pic in enumerate(images_list):
        pics_path = os.path.join(os.path.dirname(md_file_path), 'images', pic)
        ans = get_latex_table(pics_path)
        result["images/" + pic] = ans
    logger.debug("result:{}".format(result))

    # 读取Markdown文件内容
    with open(md_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    new_content = replace_images(content, result)
    # 写入
    new_md_path = os.path.join(os.path.dirname(md_file_path),
                               os.path.basename(md_file_path).split('.')[0] + '_latex.md')
    with open(new_md_path, 'w', encoding='utf-8') as file:
        file.write(new_content)
    logger.info(f"处理后的Markdown文件已保存至 {new_md_path}")


if __name__ == '__main__':
    # base_path = r'C:\Users\liuch\Documents\00\hanrui_50W\NPD2308工艺文件'
    # middle_json_name = 'middle.json'
    # path = os.path.join(base_path, middle_json_name)
    # table_image_list = parse_minerU_middle_json(path)
    # print(table_image_list)
    file_ori_path, file_out_path = '/mnt/data/llch/ForMinerU/input/测试文件样本1/2/Pic_0009.pdf', '/mnt/data/llch/ForMinerU/output'
    # ip = "127.0.0.1"
    ip = "112.48.199.7"
    response = pdf2md(file_ori_path, file_out_path)
    print(response, response['output_dir'])

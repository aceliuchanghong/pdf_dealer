import os
import sys
from pdf2image import convert_from_path
from dotenv import load_dotenv
from tqdm import tqdm

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
    return []


def extract_short_entity(rule, ocr_result_list):
    return [
        {"sure": False, "rule_name": "提取合同信息规则", "entity_name": "条形码号码", "result": "210003526766"},
        {"sure": False, "rule_name": "提取合同信息规则", "entity_name": "合同-SOB号", "result": "SOB2015"},
        {"sure": False, "rule_name": "提取合同信息规则", "entity_name": "业务员姓名", "result": "张三3"},
        {"sure": False, "rule_name": "提取合同信息规则", "entity_name": "购买方公司名称", "result": "X7X有限公司"},
    ]


if __name__ == '__main__':
    pdf_file_path = r'D:\wechatWork\WXWork\1688857567577400\Cache\File\2024-09\2024年中国AI大模型场景探索及产业应用调研报告.pdf'
    x, y = process_file(pdf_file_path)
import os
import argparse
import logging
import time
from dotenv import load_dotenv
from tqdm import tqdm
from z_utils.get_latex_table import get_latex_table
from z_utils.parse_minerU_ans import pdf2md, parse_minerU_middle_json, replace_images
from z_utils.rotate2fix_pic import detect_text_orientation
from z_utils.upload2minio import replace_image_links_in_md

load_dotenv()
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)


def process_pdf(input_pdf_path, output_path, *, rotate_pic=False, upload_pics=False):
    logger.info(f"开始MinerU-pdf转md")
    start_time = time.time()  # 记录开始时间
    logger.debug(f"输入的pdf: {input_pdf_path}, 输出路径: {output_path}")
    file_ori_path, file_out_path = input_pdf_path, output_path
    os.makedirs(file_out_path, exist_ok=True)
    basic_md_info = pdf2md(file_ori_path, file_out_path, ip=os.getenv('MinerU_ip'))
    logger.debug(f"basic_md_info: \n{basic_md_info}")
    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算耗时
    logger.info(f"MinerU转md完成，耗时: {elapsed_time:.2f}秒\n")

    logger.info(f"开始获取表格list")
    middle_json_name = os.path.basename(input_pdf_path).split('.')[0] + '_middle.json'
    base_path = basic_md_info['output_dir']
    start_time = time.time()  # 记录开始时间
    table_image_list = parse_minerU_middle_json(os.path.join(base_path, middle_json_name))
    logger.debug(f"table_image_list: \n{table_image_list}")
    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算耗时
    logger.info(f"解析middle.json获取表格完成，耗时: {elapsed_time:.2f}秒\n")

    # 图片地址
    images_path = os.path.join(base_path, 'images')
    if rotate_pic:
        logger.info(f"开始图片旋转")
        start_time = time.time()  # 记录开始时间
        images_path = os.path.join(base_path, 'rotate_images')
        logger.debug(f"rotate_images_path: {images_path}")
        os.makedirs(images_path, exist_ok=True)
        for pic_path in table_image_list:
            detect_text_orientation(os.path.join(base_path, 'images', pic_path), output_dir=images_path)
        end_time = time.time()  # 记录结束时间
        elapsed_time = end_time - start_time  # 计算耗时
        logger.info(f"图片旋转完成，耗时: {elapsed_time:.2f}秒\n")

    logger.info(f"开始获取表格latex")
    latex_result = {}
    start_time = time.time()  # 记录开始时间
    image_list = [os.path.join(images_path, file) for file in os.listdir(images_path)
                  if file.endswith('.jpg')]
    logger.debug(f"image_list: {image_list}")
    for image in tqdm(image_list, desc="表格识别中......"):
        latex = get_latex_table(image, ip=os.getenv('GOT_OCR_ip'), ocr_type="format")
        latex_result["images/" + os.path.basename(image)] = latex
    logger.debug(f"latex_result: \n{latex_result}")
    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算耗时
    logger.info(f"解析表格latex完成，耗时: {elapsed_time:.2f}秒\n")

    logger.info(f"开始生成新的md文件")
    # 读取Markdown文件内容
    original_md = basic_md_info['output_md_path']
    new_md_path = os.path.join(os.path.dirname(original_md),
                               os.path.basename(original_md).split('.')[0] + '_latex.md')
    logger.debug(f"原始md: {original_md}, 更新后md: {new_md_path}")
    start_time = time.time()  # 记录开始时间
    with open(original_md, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = replace_images(content, latex_result)
    with open(new_md_path, 'w', encoding='utf-8') as file:
        file.write(new_content)
    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算耗时
    logger.info(f"替换生成md完成，耗时: {elapsed_time:.2f}秒\n")

    if upload_pics:
        logger.info(f"开始剩余的图片上传获取链接")
        original_latex_md = new_md_path
        new_md_path = os.path.join(os.path.dirname(original_md),
                                   os.path.basename(original_md).split('.')[0] + '_latex_up.md')
        logger.debug(f"原始latex_md: {original_latex_md}, 更新后md: {new_md_path}")
        start_time = time.time()
        replace_image_links_in_md(original_latex_md, new_md_path)
        end_time = time.time()  # 记录结束时间
        elapsed_time = end_time - start_time  # 计算耗时
        logger.info(f"图片上传完成，耗时: {elapsed_time:.2f}秒\n")

    logger.info(f"result_md_path: {new_md_path}")

    return new_md_path


if __name__ == '__main__':
    """
    python pdf2md.py --input_pdf_path /mnt/data/llch/ForMinerU/input/hehe/img20240708_16193473.pdf --output_path /mnt/data/llch/ForMinerU/output --rotate_pic
    --rotate_pic
    --upload_pic
    """
    parser = argparse.ArgumentParser(description='pdf识别')
    parser.add_argument('--input_pdf_path', type=str, help='输入pdf路径')
    parser.add_argument('--output_path', default='/mnt/data/llch/ForMinerU/output', type=str, help='输出的基础路径')
    parser.add_argument('--rotate_pic', action='store_true', help='是否旋转图片')
    parser.add_argument('--upload_pic', action='store_true', help='是否上传图片')
    args = parser.parse_args()

    process_pdf(args.input_pdf_path, args.output_path, rotate_pic=args.rotate_pic)

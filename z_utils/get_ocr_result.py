import time
import requests
import logging
import os
from surya.ocr import run_ocr
from PIL import Image
from z_utils.get_model import RapidOcr_Client, Rec_processor_Client, Det_model_Client, Det_processor_Client, \
    Rec_model_Client

log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

class NewTextLine:
    def __init__(self, polygon, confidence, text, bbox):
        self.polygon = polygon
        self.confidence = confidence
        self.text = text
        self.bbox = bbox
def create_textline_from_data(data):
    polygon = data[0]  # 取出polygon坐标
    text = data[1]  # 取出OCR识别的文本
    confidence = data[2]  # 取出置信度

    # 根据polygon计算出bbox: [x_min, y_min, x_max, y_max]
    x_coords = [point[0] for point in polygon]
    y_coords = [point[1] for point in polygon]

    bbox = [min(x_coords), min(y_coords), max(x_coords), max(y_coords)]

    return NewTextLine(polygon=polygon, confidence=confidence, text=text, bbox=bbox)
def polygon_to_markdown(text_lines):
    # 将 TextLine 对象列表转换为 Markdown 格式
    markdown_text = ""
    previous_y = -1

    # 对文本框按y坐标进行排序
    sorted_lines = sorted(text_lines, key=lambda line: line.bbox[1])

    for line in sorted_lines:
        # 获取当前文本框的 y 坐标
        current_y = line.bbox[1]

        # 根据 y 坐标检测是否需要换段落
        if previous_y != -1 and abs(current_y - previous_y) > 20:
            markdown_text += "\n\n"  # 大间距时换段落
        else:
            markdown_text += " "  # 否则按空格分隔

        markdown_text += line.text
        previous_y = current_y

    return markdown_text.strip()
def run_surya_ocr(IMAGE_PATH, det_model, det_processor, rec_model, rec_processor):
    """
    ocr 结果
    """
    start_time = time.time()
    image = Image.open(IMAGE_PATH)
    langs = ["zh", "en"]
    predictions = run_ocr(
        [image], [langs], det_model, det_processor, rec_model, rec_processor
    )
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"surya_ocr耗时: {elapsed_time:.2f}秒")

    for text_line in predictions[0].text_lines:
        logger.debug(f"text_line:{text_line}")
        logger.debug(f"text:{text_line.text}")
        logger.debug(f"polygon:{text_line.polygon}")
        logger.debug(f"bbox:{text_line.bbox}")

    markdown_predictions0 = polygon_to_markdown(predictions[0].text_lines)
    markdown_predictions1 = markdown_predictions0.splitlines()
    markdown_predictions = "\n".join(
        [text for text in markdown_predictions1 if len(text) > 0]
    )
    logger.debug(f"markdown:\n{markdown_predictions}")
    return markdown_predictions

def get_latex_table(image_file, ip='112.48.199.7', ocr_type="format"):
    if ocr_type not in ["format", "ocr"]:
        raise ValueError("OCR type must be either format or ocr")
    dont_need1 = """<|im_start|>system
You should follow the instructions carefully and explain your answers in detail.<|im_end|><|im_start|>user
<img><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad></img>
OCR with format: <|im_end|><|im_start|>assistant\n"""
    dont_need2 = """<|im_start|>system
You should follow the instructions carefully and explain your answers in detail.<|im_end|><|im_start|>user
<img><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad></img>
OCR: <|im_end|><|im_start|>assistant\n"""
    url = f"http://{ip}:9522/run-ocr/"
    data = {
        "image_file": image_file,
        "ocr_type": ocr_type,
    }
    start_time = time.time()
    response = requests.post(url, params=data)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug(f"花费: {elapsed_time} s,ocr结果:\n{response.json()}")
    ans = response.json()['output'].replace(dont_need1, '').replace(dont_need2, '')
    return ans


def easy_ocr(image_file):
    ans = ''
    ocr_client = RapidOcr_Client()
    start_time = time.time()
    rapid_ocr_result, _ = ocr_client(image_file)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug(f"rapid-OCR耗时: {elapsed_time:.2f}秒")

    text_lines = []
    for line in rapid_ocr_result:
        text_line = create_textline_from_data(line)
        text_lines.append(text_line)
    markdown0 = polygon_to_markdown(text_lines)
    markdown1 = markdown0.splitlines()[: int(os.getenv("import_head_lines"))]
    rapid_ocr_markdown = "\n".join([text for text in markdown1 if len(text) > 0])
    logger.info(f"rapid_ocr_markdown:{rapid_ocr_markdown}")


    rec_processor = Rec_processor_Client()
    det_model = Det_model_Client()
    det_processor = Det_processor_Client()
    rec_model = Rec_model_Client()

    surya_ocr_result = run_surya_ocr(
        image_file,
        det_model,
        det_processor,
        rec_model,
        rec_processor,
    )
    logger.info(f"surya_ocr_result:{surya_ocr_result}")

    return rapid_ocr_markdown + surya_ocr_result


if __name__ == '__main__':
    image_file = '/mnt/data/llch/GOT-OCR2.0/input/test2.jpg'
    # rotate_image = detect_text_orientation(image_file, '/mnt/data/llch/GOT-OCR2.0/output')
    ans = get_latex_table(image_file, ocr_type='ocr')
    print(ans)

import time
import requests
import logging
import os

from z_utils.rotate2fix_pic import detect_text_orientation

log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)


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


if __name__ == '__main__':
    image_file = '/mnt/data/llch/GOT-OCR2.0/input/test2.jpg'
    # rotate_image = detect_text_orientation(image_file, '/mnt/data/llch/GOT-OCR2.0/output')
    ans = get_latex_table(image_file, ocr_type='ocr')
    print(ans)

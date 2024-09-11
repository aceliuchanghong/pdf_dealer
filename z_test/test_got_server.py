import time
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    dont_need = """<|im_start|>system
You should follow the instructions carefully and explain your answers in detail.<|im_end|><|im_start|>user
<img><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad><imgpad></img>
OCR with format: <|im_end|><|im_start|>assistant\n"""
    # ip = "127.0.0.1"
    ip = "112.48.199.7"
    url = f"http://{ip}:9522/run-ocr/"
    image_file = '/mnt/data/llch/ForMinerU/input/测试文件样本1/2/Pic_0010.pdf_show_0.jpg'
    data = {
        "image_file": image_file,
    }
    start_time = time.time()
    response = requests.post(url, params=data)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"花费: {elapsed_time} s")
    print(response.json()['output'].replace(dont_need, ''))

    if response.status_code == 200:
        try:
            json_response = response.json()  # 尝试解析为JSON
            logger.debug(f"Success: {json_response}")
        except ValueError:
            logger.error(f"Response is not valid JSON: {response.text}")  # 如果不是JSON，输出文本内容
    else:
        logger.error(f"Error: status_code: {response.status_code}, response: {response.text}")  # 直接输出响应内容
